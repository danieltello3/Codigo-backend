import { Response } from "express";
import { Producto } from "../producto/producto.model";
import { RequestUser } from "../utils/validador";
import { IMovimiento, Movimiento } from "./movimiento.model";
import { configure } from "mercadopago";
import dotenv from "dotenv";
import { CreatePreferencePayload } from "mercadopago/models/preferences/create-payload.model";
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
   const preferencia: CreatePreferencePayload = {
      auto_return: "approved",
      back_urls: {
         success: "http://127.0.0.1:8000/success",
         failure: "http://127.0.0.1:8000/failure",
         pending: "http://127.0.0.1:8000/pending",
      },
      items: [
         {
            id: "123",
            title: "titulo del producto",
            description: "descripcion del producto",
            picture_url: "http://imagen.com",
            category_id: "id",
            quantity: 1,
            currency_id: "PEN",
            unit_price: 40.8,
         },
      ],
      payer: {
         name: "Daniel",
         surname: "Tello",
         email: "test_user_46542185@testuser.com",
         phone: {
            area_code: "51",
            number: "999036353",
         },
         identification: {
            type: "DNI",
            number: "22145428",
         },
         address: {
            zip_code: "04002",
            street_name: "Av Primavera",
            street_number: "1150",
         },
         date_created: "2021-07-21",
      },
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
      console.log(movimiento?.movimientoDetalles);

      return res.json({
         success: true,
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
