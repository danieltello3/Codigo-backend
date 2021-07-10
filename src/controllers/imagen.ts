import { Request, Response } from "express";
import { Imagen } from "../config/models";
import { subirArchivoUtil } from "../utils/manejoArchivoFirebase";
import { TRespuesta } from "./dto.response";

export const subirImagen = async (req: Request, res: Response) => {
   console.log(req.file);
   const { carpeta } = req.query;
   if (!carpeta) {
      return res.status(400).json({
         message: " falta la carpeta de destino",
      });
   }

   if (req.file) {
      try {
         const archivo = req.file;
         const archivoArray = req.file.originalname.split(".");
         const extension = archivoArray[archivoArray.length - 1];
         const archivo_sin_extension = req.file.originalname.replace(
            `.${extension}`,
            ""
         );
         const nombre_archivo = `${archivo_sin_extension}_${Date.now()}`;
         archivo.originalname = `${nombre_archivo}.${extension}`;

         const link = await subirArchivoUtil(archivo, String(carpeta));

         const nuevaImagen = await Imagen.create({
            imagenNombre: nombre_archivo,
            imagenExtension: extension,
            imagenPath: carpeta,
         });

         const content = { ...nuevaImagen.toJSON(), link };
         const rpta: TRespuesta = {
            message: "Archivo subido exitosamente",
            content: content,
            success: true,
         };
         return res.status(200).json(rpta);
      } catch (error) {
         const rpta: TRespuesta = {
            message: "error al subir la imagen",
            content: null,
            success: false,
         };
         return res.status(400).json(rpta);
      }
   }
};
