import { NextFunction, Request, Response } from "express";

type TActualizarProducto = {
   productoNombre: string;
   productoPrecio: number;
   productoImagen: string;
   productoTipo: "LATTES" | "COMIDA" | "MERCHANDISING" | "FRAPPS";
};

export const actualizarProductoDto = (
   req: Request,
   res: Response,
   next: NextFunction
) => {
   const data: TActualizarProducto = req.body;
   const tipos = ["LATTES", "COMIDA", "MERCHANDISING", "FRAPPS"];

   const resultadoTipo = tipos.filter((tipo) => tipo == data.productoTipo)[0];

   if (
      data.productoNombre &&
      data.productoImagen &&
      data.productoPrecio &&
      data.productoTipo &&
      resultadoTipo
   ) {
      next();
   } else {
      const rpta = {
         success: false,
         content: null,
         message: "Falta campos",
      };
      return res.status(400).json(rpta);
   }
};
