import { Router } from "express";
import { tipoRequestDto } from "../controllers/dto.request";
import { crearTipo, listarTipos } from "../controllers/tipo";

export const tipoRouter = Router();

tipoRouter.route("/tipos").post(tipoRequestDto, crearTipo).get(listarTipos);
