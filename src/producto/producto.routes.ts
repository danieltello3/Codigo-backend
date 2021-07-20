import { Router } from "express";
import { actualizarProductoDto } from "./dto.request";
import {
   actualizarProducto,
   crearProducto,
   eliminarProducto,
   mostrarProductos,
} from "./producto.controller";

export const productoRouter = Router();

productoRouter.route("/productos").post(crearProducto).get(mostrarProductos);

productoRouter
   .route("/productos/:id")
   .patch(actualizarProducto)
   .put(actualizarProductoDto, actualizarProducto)
   .delete(eliminarProducto);
