import { Router } from "express";
import { accionRequestDto } from "../controllers/dto.request";
import { crearAccion } from "../controllers/accion";

export const accionRouter = Router();

accionRouter.route("/acciones").post(accionRequestDto, crearAccion);
