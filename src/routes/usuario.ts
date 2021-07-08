import { Router } from "express";
import { loginRequestDto } from "../controllers/dto.request";
import { login, registro } from "../controllers/usuario";

export const usuarioRouter = Router();

usuarioRouter.post("/registro", registro);
usuarioRouter.post("/login", loginRequestDto, login);
