import { NextFunction, Request, Response } from "express";
import fetch from "node-fetch";
import dotenv from "dotenv";

dotenv.config();

enum tipoUsuario {
   CLIENTE = "CLIENTE",
   PERSONAL = "PERSONAL",
}

interface IRptaApiPeru {
   success: boolean;
   data?: {
      numero: string;
      nombre_completo: string;
      nombres: string;
      apellido_paterno: string;
      apellido_materno: string;
      codigo_verificacion: number;
   };
   message?: string;
}

type TRegistro = {
   usuarioCorreo: string;
   usuarioTelefono?: string;
   usuarioNombre?: string;
   usuarioApellido?: string;
   usuarioDni: string;
   usuarioPassword?: string;
   usuarioDireccion?: {
      zip: string;
      calle: string;
      numero: number;
   };
   usuarioTipo: tipoUsuario;
};

export const registroDto = async (
   req: Request,
   res: Response,
   next: NextFunction
) => {
   const data: TRegistro = req.body;
   if (
      data.usuarioDni &&
      data.usuarioCorreo &&
      data.usuarioPassword &&
      data.usuarioTipo
   ) {
      /* se busca usuario en la reniec */

      const respuesta = await fetch(
         `${process.env.BASE_URL_API_PERU}${data.usuarioDni}`,
         {
            method: "GET",
            headers: {
               Authorization: `Bearer ${process.env.API_PERU_TOKEN}`,
               "Content-Type": "application/json",
            },
         }
      );

      const userApi: IRptaApiPeru = await respuesta.json();
      console.log(userApi);
      if (userApi.success === false) {
         return res.status(400).json({
            success: false,
            content: null,
            message: userApi.message,
         });
      }

      data.usuarioNombre = userApi?.data?.nombres;
      data.usuarioApellido = `${userApi?.data?.apellido_paterno} ${userApi?.data?.apellido_materno}`;

      if (data.usuarioTipo == tipoUsuario.PERSONAL && data?.usuarioPassword) {
         next();
      } else {
         if (data.usuarioTipo === tipoUsuario.CLIENTE) {
            if (data.usuarioDireccion && data.usuarioTelefono) {
               next();
            } else {
               return res.status(400).json({
                  success: false,
                  content: null,
                  message: "Error al crear al cliente, faltan campos",
               });
            }
         } else {
            return res.status(400).json({
               success: false,
               content: null,
               message: "Error al crear el personal, faltan campos",
            });
         }
      }
   } else {
      return res.status(400).json({
         success: false,
         content: null,
         message: "Error al crear el personal, faltan campos",
      });
   }
};
