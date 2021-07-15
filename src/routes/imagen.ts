import { NextFunction, Request, Response, Router } from "express";
import Multer from "multer";
import { eliminarArchivo, subirImagen } from "../controllers/imagen";

const multer = Multer({
   storage: Multer.memoryStorage(),
   //    limits: {
   //       // tamaño maximo del archivo, expresado en bytes
   //       fileSize: 5 * 1024 * 1024,
   //    },
});

export const imagenRouter = Router();

imagenRouter.post(
   "/subirImagen",
   multer.single("imagen"),
   (req: Request, res: Response, next: NextFunction) => {
      const size = req.file?.size;
      if (size && size <= 5242880) {
         next();
      } else {
         return res.status(400).json({
            message: "el archivo es muy grande",
         });
      }
   },
   subirImagen
);

imagenRouter.delete("/eliminarImagen", eliminarArchivo);
