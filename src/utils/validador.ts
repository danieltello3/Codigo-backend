import { Request, Response, NextFunction } from "express";
import { verify } from "jsonwebtoken";
import dotenv from "dotenv";
import { TRespuesta } from "../controllers/dto.response";
import { BlackList, Usuario } from "../config/models";
import { Model } from "sequelize";

dotenv.config();

export interface RequestCustom extends Request {
   user?: Model | null;
}

const verificarToken = (token: string) => {
   try {
      const payload = verify(token, String(process.env.JWT_SECRET));
      return payload;
   } catch (error) {
      console.log(error.message);
      return error.message;
   }
};

export const authValidator = async (
   req: RequestCustom,
   res: Response,
   next: NextFunction
) => {
   //primero se valida si recibe la token x authorization, sino se retorna un estado 401
   if (!req.headers.authorization) {
      const rpta: TRespuesta = {
         content: null,
         message: "se necesita una token en authorization",
         success: false,
      };
      return res.status(401).json(rpta);
   }

   const token = req.headers.authorization.split(" ")[1];

   //si encuentra el token el blacklist, retornara un modelo, sino retornara null
   const tokenBL = await BlackList.findOne({
      where: { blackListToken: token },
   });

   if (tokenBL === null) {
      const respuesta = verificarToken(token);

      console.log(respuesta);

      if (typeof respuesta === "object") {
         console.log("token valida");
         const usuario = await Usuario.findByPk(respuesta.usuarioId, {
            attributes: { exclude: ["usuarioPassword"] },
            raw: true,
         });
         req.user = usuario;
         next();
      } else {
         const rpta: TRespuesta = {
            success: false,
            content: null,
            message: "Token invalida",
         };
         return res.status(401).json(rpta);
      }
   } else {
      const rpta: TRespuesta = {
         success: false,
         content: null,
         message: "Token ya fue usada, necesita generar una nueva",
      };
      return res.status(401).json(rpta);
   }
};
