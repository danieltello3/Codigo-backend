import { Request, Response } from "express";
import { Producto } from "../producto/producto.model";
import { RequestUser } from "../utils/validador";
import { IMovimiento, Movimiento } from "./movimiento.model";
import { configure, payment, preferences } from "mercadopago";
import dotenv from "dotenv";
import {
   CreatePreferencePayload,
   PreferenceItem,
} from "mercadopago/models/preferences/create-payload.model";
import { Usuario } from "../usuario/usuario.model";
import fetch from "node-fetch";
dotenv.config();

interface ILMovimiento extends Omit<IMovimiento, "vendedorId"> {}

export const crearMovimiento = async (req: RequestUser, res: Response) => {
   const vendedor = req.user._id;
   const {
      movimientoFecha,
      movimientoTipo,
      movimientoDetalles,
      usuarioId,
   }: ILMovimiento = req.body;
   try {
      const usuario = await Usuario.findById(usuarioId);
      if (!usuario) {
         throw new Error("el usuario no existe");
      }
      await Promise.all(
         movimientoDetalles.map(async (detalle) => {
            const producto = await Producto.findById(detalle.productoId);
            if (!producto) {
               throw new Error(`No existe el producto ${detalle.productoId}`);
            }
            detalle.detallePrecio = Number(producto?.productoPrecio);
         })
      );
      const movimiento: IMovimiento = {
         movimientoFecha,
         movimientoTipo,
         movimientoDetalles,
         usuarioId,
         vendedorId: vendedor,
         movimientoPasarela: {},
      };

      const nuevoMovimiento = await Movimiento.create(movimiento);

      return res.status(201).json({
         success: true,
         content: nuevoMovimiento,
         message: "movimiento creado exitosamente",
      });
   } catch (error) {
      console.log(error);

      return res.status(400).json({
         success: false,
         content: error.message,
         message: "Error al crear el movimiento",
      });
   }
};

export const crearPreferencia = async (req: RequestUser, res: Response) => {
   configure({
      access_token: String(process.env.ACCESS_TOKEN_MP),
      integrator_id: String(process.env.INTEGRATOR_ID_MP),
   });
   const payload: any = {
      auto_return: "approved",
      notification_url: process.env.NOTIFICATION_URL,
      back_urls: {
         success: process.env.SUCCESS_URL,
         failure: process.env.FAILURE_URL,
         pending: process.env.PENDING_URL,
      },
      // items: [
      //    {
      //       id: "123",
      //       title: "titulo del producto",
      //       description: "descripcion del producto",
      //       picture_url: "http://imagen.com",
      //       category_id: "id",
      //       quantity: 1,
      //       currency_id: "PEN",
      //       unit_price: 40.8,
      //    },
      // ],
      // payer: {
      //    name: "Daniel",
      //    surname: "Tello",
      //    email: "test_user_46542185@testuser.com",
      //    phone: {
      //       area_code: "51",
      //       number: 999036353,
      //    },
      //    identification: {
      //       type: "DNI",
      //       number: "22145428",
      //    },
      //    address: {
      //       zip_code: "04002",
      //       street_name: "Av Primavera",
      //       street_number: 1150,
      //    },
      //    date_created: "2021-07-21",
      // },
      payment_methods: {
         excluded_payment_methods: [
            {
               id: "master",
            },
            {
               id: "debvisa",
            },
         ],
         installments: 3,
      },
   };
   const { movimientoId } = req.body;
   try {
      const movimiento = await Movimiento.findById(movimientoId);

      if (!movimiento) {
         throw new Error(`El movimiento ${movimientoId} no existe`);
      }

      const usuario = await Usuario.findById(movimiento.usuarioId);
      if (!usuario) {
         throw new Error("Usuario no encontrado");
      }

      payload.payer = {
         name: usuario.usuarioNombre,
         surname: usuario.usuarioApellido,
         address: {
            zip_code: usuario.usuarioDireccion?.zip ?? "",
            street_name: usuario.usuarioDireccion?.calle ?? "",
            street_number: usuario.usuarioDireccion?.numero ?? 0,
         },
         phone: {
            area_code: "51",
            number: usuario.usuarioTelefono ? +usuario.usuarioTelefono : 0,
         },
         email: "test_user_46542185@testuser.com",
         identification: {
            type: "DNI",
            number: usuario.usuarioDni,
         },
      };
      const host = req.get("host") ?? "";
      let items: PreferenceItem[] = [];
      await Promise.all(
         movimiento.movimientoDetalles.map(async (detalle) => {
            const producto = await Producto.findById(detalle.productoId);
            if (producto) {
               items.push({
                  id: detalle.productoId,
                  title: producto?.productoNombre,
                  description: "descripcion del producto",
                  picture_url: host + producto?.productoImagen,
                  category_id: producto?.productoTipo,
                  quantity: detalle.detalleCantidad,
                  currency_id: "PEN",
                  unit_price: +producto?.productoPrecio,
               });
            }
         })
      );

      payload.items = items;
      const preferencia = await preferences.create(payload);

      movimiento.movimientoPasarela.collectorId =
         preferencia.response.collector_id;
      await movimiento.save();

      return res.json({
         success: true,
         content: preferencia.response.init_point,
         message: null,
      });
   } catch (error) {
      console.log(error);

      return res.status(404).json({
         success: false,
         content: null,
         message: error.message,
      });
   }
};

export const mpEventos = async (req: Request, res: Response) => {
   // console.log("BODY: ");
   // console.log(req.body);
   // console.log("---------------------------------------------------");
   // console.log("QUERY PARAMS:");
   // console.log(req.query);
   const { id, topic } = req.query;

   if (topic === "payment") {
      console.log("=====================================");
      console.log(id);
      const pago = await payment.get(Number(id), {
         headers: { Authorization: `Bearer ${process.env.ACCESS_TOKEN_MP}` },
      });

      console.log("Aqui se muestra pago");

      const {
         payment_method_id,
         payment_type_id,
         status,
         status_detail,
         collector_id,
      } = pago.body;
      const movimiento = await Movimiento.findOne({
         "movimientoPasarela.collectorId": collector_id,
      });
      let first_six_digits;
      if (
         payment_type_id === "credit_card" ||
         payment_type_id === "debit_card"
      ) {
         first_six_digits = pago.body.card.first_six_digits;
      }
      if (movimiento) {
         movimiento.movimientoPasarela.paymentMethodId = payment_method_id;
         movimiento.movimientoPasarela.paymentTypeId = payment_type_id;
         movimiento.movimientoPasarela.status = status;
         movimiento.movimientoPasarela.statusDetail = status_detail;
         movimiento.movimientoPasarela.firstSixDigits = first_six_digits;
         await movimiento.save();
      }

      //console.log("Aqui se muestra el fetch");
      // const response = await fetch(
      //    `https://api.mercadopago.com/v1/payments/${id}`,
      //    {
      //       headers: { Authorization: `Bearer ${process.env.ACCESS_TOKEN_MP}` },
      //    }
      // );
      // const json = await response.json();
      // console.log(json.status);
   }

   return res.status(200).json({});
};

export const listarMovimientos = async (req: Request, res: Response) => {
   const movimientos = await Movimiento.find();
   return res.json({
      success: true,
      content: movimientos,
      message: null,
   });
};
