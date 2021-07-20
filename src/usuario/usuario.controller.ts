import { compareSync } from "bcrypt";
import { Request, Response } from "express";
import { Usuario } from "./usuario.model";
import { sign } from "jsonwebtoken";
import dotenv from "dotenv";
dotenv.config();

export const registro = async (req: Request, res: Response) => {
   console.log(req.body);
   try {
      const nuevoUsuario = await Usuario.create(req.body);
      delete nuevoUsuario._doc["usuarioPassword"];
      return res.json({
         success: true,
         content: nuevoUsuario,
         message: "Usuario creado exitosamente",
      });
   } catch (error) {
      console.log(error);
      return res.status(400).json({
         success: false,
         message: "error al crear al usuario",
      });
   }
};

export const login = async (req: Request, res: Response) => {
   const { correo, password } = req.body;
   try {
      const usuario = await Usuario.findOne(
         { usuarioCorreo: correo },
         "usuarioPassword usuarioTipo"
      );
      console.log(usuario);
      // if (!usuario || usuario.usuarioTipo === "CLIENTE") {
      //    return res.status(404).json({
      //       success: false,
      //       message: "credenciales invalidas",
      //       content: null,
      //    });
      // }

      const resultado = compareSync(password, usuario.usuarioPassword);
      if (resultado) {
         //generamos JWT
         const payload = {
            usuarioId: usuario._id,
         };
         const token = sign(payload, process.env.JWT_SECRET ?? "", {
            expiresIn: "1h",
         });
         return res.status(200).json({
            success: true,
            content: token,
            message: "login exitoso",
         });
      } else {
         return res.status(400).json({
            success: false,
            message: "credenciales invalidas",
            content: null,
         });
      }
   } catch (error) {
      console.log(error);
      return res.status(404).json({
         success: false,
         message: "error al obtener el usuario",
      });
   }
};
