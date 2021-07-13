import { Request, Response } from "express";
import { Movimiento, DetalleMovimiento } from "../config/models";
import { conexion } from "../config/sequelize";
import { RequestCustom } from "../utils/validador";
import { TMovimientoRequest } from "./dto.request";
import { TRespuesta } from "./dto.response";

export const crearMovimiento = async (req: RequestCustom, res: Response) => {
   const transaccion = await conexion.transaction();
   try {
      const {
         movimientoFecha,
         movimientoTipo,
         movimientoDetalle,
      }: TMovimientoRequest = req.body;
      const nuevoMovimiento = await Movimiento.create(
         {
            movimientoFecha,
            movimientoTipo,
            movimientoTotal: 0.0,
            usuarioId: req.user?.getDataValue("usuarioId"),
         },
         { transaction: transaccion }
      );
      let total = 0.0;
      const movimientoDetalles = await Promise.all(
         movimientoDetalle.map(
            async ({
               detalleMovimientoCantidad,
               detalleMovimientoPrecio,
               productoId,
            }) => {
               total += detalleMovimientoCantidad * detalleMovimientoPrecio;

               return await DetalleMovimiento.create(
                  {
                     detalleMovimientoCantidad,
                     detalleMovimientoPrecio,
                     productoId,
                     movimientoId: nuevoMovimiento.getDataValue("movimientoId"),
                  },
                  { transaction: transaccion }
               );
            }
         )
      );
      nuevoMovimiento.setDataValue("movimientoTotal", total);
      await nuevoMovimiento.save({ transaction: transaccion });
      await transaccion.commit();
      const rpta: TRespuesta = {
         success: true,
         message: "Movimiento creado exitosamente",
         content: null,
      };
      return res.status(201).json(rpta);
   } catch (error) {
      await transaccion.rollback();

      const rpta: TRespuesta = {
         success: false,
         message: "Error al crear el movimiento",
         content: error.message,
      };
      return res.status(400).json(rpta);
   }
};
