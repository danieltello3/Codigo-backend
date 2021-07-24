import { Router } from "express";
import { authValidator, personalValidator } from "../utils/validador";
import {
   crearMovimiento,
   crearPreferencia,
   listarMovimientos,
   mpEventos,
} from "./movimiento.controller";

export const movimientoRouter = Router();

movimientoRouter
   .route("/movimientos")
   .post(authValidator, crearMovimiento)
   .get(listarMovimientos);
movimientoRouter.post(
   "/venta",
   authValidator,
   personalValidator,
   crearPreferencia
);

movimientoRouter.post("/mercadopago-ipn", mpEventos);
