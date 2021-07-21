import { Response } from "express";
import { RequestUser } from "../utils/validador";

export const crearMovimiento = (req: RequestUser, res: Response) => {
   const { movimientoFecha, movimientoTipo, movimientoDetalles, usuarioId } =
      req.body;

   movimientoDetalles.forEach(
      (detalle: { detalleCantidad: number; detalleProducto: string }) => {}
   );
   console.log(req.user);
   res.json({
      success: true,
   });
};
