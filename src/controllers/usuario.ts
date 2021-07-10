import { compareSync } from "bcrypt";
import { Request, Response } from "express";
import { sign } from "jsonwebtoken";
import { BlackList, Imagen, Usuario } from "../config/models";
import { RequestCustom } from "../utils/validador";
import { generarUrl } from "../utils/manejoArchivoFirebase";
import { TRespuesta } from "./dto.response";
import dotenv from "dotenv";

dotenv.config();

export const registro = async (
   req: Request,
   res: Response
): Promise<Response> => {
   try {
      const {
         email: usuarioCorreo,
         password: usuarioPassword,
         nombre: usuarioNombre,
         tipo: tipoId,
         imagenId,
      } = req.body;
      const nuevoUsuario = await Usuario.create({
         usuarioCorreo,
         usuarioPassword,
         usuarioNombre,
         tipoId,
         imagenId,
      });

      const usuarioEncontrado = await Usuario.findOne({
         attributes: {
            exclude: ["usuarioPassword"],
         },
         where: { usuarioId: nuevoUsuario.getDataValue("usuarioId") },
         include: { model: Imagen },
      });
      const imagen = usuarioEncontrado?.getDataValue("imagen");

      const url = await generarUrl(
         imagen.imagenPath,
         `${imagen.imagenNombre}.${imagen.imagenExtension}`
      );

      const respuesta = { ...usuarioEncontrado?.toJSON(), imagenUrl: url };
      //nuevoUsuario.setDataValue("usuarioPassword", null);
      const rpta: TRespuesta = {
         content: respuesta,
         message: "Usuario creado exitosamente",
         success: true,
      };
      return res.status(201).json(rpta);
   } catch (error) {
      const rpta: TRespuesta = {
         content: error,
         message: "Error al crear el usuario",
         success: false,
      };
      return res.status(400).json(rpta);
   }

   //metodo 2
   //    const nuevoUsuario = Usuario.build(req.body)
   //    const passwordEncriptada = hashSync(req.body.usuarioPassword, 10)
   //    nuevoUsuario.setDataValue('usuarioPassword', passwordEncriptada)
   //    nuevoUsuario.save()
   //    const rpta: TRespuesta = {
   //     content: nuevoUsuario,
   //     message: "Usuario creado exitosamente",
   //     success: true,
   //     };
   //     return res.status(201).json(rpta)
};

export const login = async (req: Request, res: Response) => {
   const { email, password } = req.body;
   const usuario = await Usuario.findOne({ where: { usuarioCorreo: email } });
   if (usuario) {
      const resultado = compareSync(
         password,
         usuario.getDataValue("usuarioPassword")
      );
      console.log(resultado);
      if (resultado) {
         //si resultado es true, el correo y la password son correctas
         const payload = {
            usuarioId: usuario.getDataValue("usuarioId"),
         };
         const token = sign(payload, String(process.env.JWT_SECRET), {
            expiresIn: "1h",
         });

         const rpta: TRespuesta = {
            success: true,
            content: token,
            message: "ok",
         };
         return res.status(200).json(rpta);
      }
   }
   const rpta: TRespuesta = {
      success: false,
      content: null,
      message: "Credenciales incorrectas",
   };
   return res.status(404).json(rpta);
};

export const perfil = async (
   req: RequestCustom,
   res: Response
): Promise<Response> => {
   const imagenId = req?.user?.getDataValue("imagenId");
   const imagen_encontrada = await Imagen.findByPk(imagenId);
   const url = await generarUrl(
      imagen_encontrada?.getDataValue("imagenPath"),
      `${imagen_encontrada?.getDataValue(
         "imagenNombre"
      )}.${imagen_encontrada?.getDataValue("imagenExtension")}`
   );

   const content = { ...req?.user?.toJSON(), url };

   const rpta: TRespuesta = {
      content,
      success: true,
      message: ".",
   };
   return res.json(rpta);
};

export const logout = async (req: Request, res: Response) => {
   if (!req.headers.authorization) {
      const rpta: TRespuesta = {
         content: null,
         message:
            "Error al hacer el logout, se necesita una token en el header",
         success: false,
      };
      return res.status(400).json(rpta);
   }
   const token = req.headers.authorization.split(" ")[1];
   try {
      await BlackList.create({ blackListToken: token });
      return res.status(204).send();
   } catch (error) {
      const rpta: TRespuesta = {
         content: error.message,
         message: "Error al hacer el logout",
         success: false,
      };
      return res.status(400).json(rpta);
   }
   //el estado 204 se usa para indicar que la operacion fue realizada exitosamente pero no se retorna nada. (no hay contenido)
};
