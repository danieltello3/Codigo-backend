import { Router } from "express";
import { loginRequestDto } from "../controllers/dto.request";
import { login, logout, perfil, registro } from "../controllers/usuario";
import { authValidator } from "../utils/validador";

export const usuarioRouter = Router();

usuarioRouter.post("/registro", registro);
usuarioRouter.post("/login", loginRequestDto, login);
usuarioRouter.get("/perfil", authValidator, perfil);
usuarioRouter.post("/logout", logout);
