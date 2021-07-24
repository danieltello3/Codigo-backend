import { JwtPayload, verify } from "jsonwebtoken";
import dotenv from "dotenv";
import { Request, Response, NextFunction } from "express";
import { Usuario } from "../usuario/usuario.model";
dotenv.config();

export interface RequestUser extends Request {
   user?: any;
}

const verificarToken = (token: string): JwtPayload | string => {
   try {
      const payload = verify(token, String(process.env.JWT_SECRET));
      return payload;
   } catch (error: any) {
      return error.message;
   }
};

export const authValidator = async (
   req: RequestUser,
   res: Response,
   next: NextFunction
) => {
   if (!req.headers.authorization) {
      return res.status(401).json({
         success: false,
         content: null,
         message: "se necesita una token para este request",
      });
   }
   const token = req.headers.authorization.split(" ")[1];
   const resultado = verificarToken(token);

   if (typeof resultado === "object") {
      const id = resultado.usuarioId;
      const usuario = await Usuario.findById(id, "-usuarioPassword");
      req.user = usuario;
      next();
   } else {
      return res.status(401).json({
         success: false,
         content: resultado,
         message: "Token invalida",
      });
   }
};

export const personalValidator = async (
   req: RequestUser,
   res: Response,
   next: NextFunction
) => {
   if (req.user?.usuarioTipo === "PERSONAL") {
      next();
   } else {
      return res.status(401).json({
         success: false,
         content: null,
         message: "Usuario no dispone de privilegios suficientes",
      });
   }
};
