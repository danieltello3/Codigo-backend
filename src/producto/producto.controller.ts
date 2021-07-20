import { Request, Response } from "express";
import {
   paginatedHelper,
   paginationSerializer,
} from "../utils/pagination.helper";
import { Producto } from "./producto.model";

export const crearProducto = async (req: Request, res: Response) => {
   try {
      const nuevoProducto = await Producto.create(req.body);
      return res.status(201).json({
         success: true,
         content: nuevoProducto,
         message: "Producto creado exitosamente",
      });
   } catch (error) {
      return res.status(400).json({
         success: false,
         content: error,
         message: "Error al crear el producto",
      });
   }
};

export const mostrarProductos = async (req: Request, res: Response) => {
   const page = Number(req.query?.page) ?? 1;
   const perPage = Number(req.query?.perPage) ?? 1;

   const pagination = { page, perPage };

   const paginationParams = paginatedHelper(pagination);

   const [count, resultado] = await Promise.all([
      Producto.estimatedDocumentCount(),
      Producto.find({}, {}, { ...paginationParams }),
   ]);

   const pageInfo = paginationSerializer(count, pagination);

   return res.status(200).json({
      success: true,
      content: { pageInfo, resultado },
      message: "ok",
   });
};

export const actualizarProducto = async (req: Request, res: Response) => {
   const { id } = req.params;
   try {
      const productoActualizado = await Producto.findOneAndUpdate(
         { _id: id },
         { $set: req.body },
         { new: true }
      );

      return res.status(201).json({
         success: true,
         content: productoActualizado,
         message: "producto actualizado exitosamente",
      });
   } catch (error) {
      return res.status(400).json({
         success: false,
         content: error,
         message: "Error al actualizar el producto",
      });
   }
};

export const eliminarProducto = async (req: Request, res: Response) => {
   const { id } = req.params;
   try {
      const productoEliminado = await Producto.findByIdAndDelete(id);

      return res.status(200).json({
         success: true,
         content: productoEliminado,
         message: "Producto Eliminado exitosamente",
      });
   } catch (error) {
      return res.status(400).json({
         success: false,
         content: error,
         message: "Error al eliminar el producto",
      });
   }
};
