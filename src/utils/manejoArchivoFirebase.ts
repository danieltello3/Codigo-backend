import { Storage } from "@google-cloud/storage";
import { Express } from "express";
//creo la instancia de la clase Storage con la configuracion de las credenciales y el id del proyecto

const storage = new Storage({
   projectId: "zapateria-codigo-daniel",
   keyFilename: "./credenciales_firebase.json",
});

//Enlazo mi bucket (donde se almacenaran todas las imagenes)

const bucket = storage.bucket("zapateria-codigo-daniel.appspot.com");

export const subirArchivoUtil = (
   archivo: Express.Multer.File,
   path: string
): Promise<string> => {
   return new Promise((resolve, reject) => {
      if (!archivo) {
         reject("No se encontro el archivo");
      }

      //comienza el proceso de subida de imagenes
      const new_file = bucket.file(`${path}/${archivo.originalname}`);

      // agregar configuracion adicional de nuestro archivo como su metadata
      const blobStream = new_file.createWriteStream({
         metadata: {
            contentType: archivo.mimetype,
         },
      });

      //ahora puedo escuchar eventos
      blobStream.on("error", (e) => {
         reject(e.message);
      });

      //veremos el evento si es que la carga termino exitosamente
      blobStream.on("finish", async () => {
         try {
            const link = await new_file.getSignedUrl({
               action: "read",
               expires: Date.now() + 1000 * 60 * 60,
            });
            resolve(link.toString());
         } catch (error) {
            reject(error);
         }
      });

      //aca se le indica que el procedimiento terminara pero para que gestione toda la transferencia del archivo, se le enviara sus bytes
      blobStream.end(archivo.buffer);
   });
};

export const generarUrl = async (
   carpeta: string,
   filename: string
): Promise<string> => {
   try {
      const url = await bucket.file(`${carpeta}/${filename}`).getSignedUrl({
         action: "read",
         expires: Date.now() + 1000 + 60 + 60,
      });
      return url.toString();
   } catch (error) {
      return error;
   }
};

export const eliminarAtchivoUtil = async (carpeta: string, archivo: string) => {
   try {
      const respuesta = await bucket
         .file(`${carpeta}/${archivo}`)
         .delete({ ignoreNotFound: true });
      console.log(respuesta);
      return respuesta;
   } catch (error) {
      return error;
   }
};
