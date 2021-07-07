import { Tipo } from "../config/models";
import { Request, Response } from "express";
import { TRespuesta } from "./dto.response";

export const crearTipo = async (
   req: Request,
   res: Response
): Promise<Response> => {
   // usar try-catch siempre que usemos async-await, para metodos de creacion, edicion y eliminacion
   try {
      const nuevoTipo = await Tipo.create(req.body);

      const rpta: TRespuesta = {
         success: true,
         message: "tipo creado exitosamente",
         content: nuevoTipo,
      };
      return res.status(201).json(rpta);
   } catch (error) {
      console.log(error);
      const rpta: TRespuesta = {
         success: false,
         message: `Error al crear el tipo`,
         content: error.message,
      };
      return res.status(400).json(rpta);
   }
};

//retornar todos los tipos

export const listarTipos = async (
   req: Request,
   res: Response
): Promise<Response> => {
   const tipos = await Tipo.findAll();
   const rpta: TRespuesta = {
      success: true,
      message: "ok",
      content: tipos,
   };
   return res.status(200).json(rpta);
};
