import express, { Response, Request, NextFunction } from "express";
import { json } from "body-parser";
import { connect } from "mongoose";
import dotenv from "dotenv";
import { productoRouter } from "../producto/producto.routes";

dotenv.config();

export default class Server {
   app;
   port: Number;

   constructor() {
      this.app = express();
      this.port = Number(process.env.PORT) || 8000;
      this.bodyParser();
      this.CORS();
      this.rutas();
   }

   bodyParser() {
      this.app.use(json());
   }

   rutas() {
      this.app.get("/", (req: Request, res: Response) => {
         res.json({
            success: true,
         });
      });
      this.app.use("/api", productoRouter);
   }

   CORS() {
      this.app.use((req: Request, res: Response, next: NextFunction) => {
         res.header("Access-Control-Allow-Origin", "*");
         res.header(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization"
         ),
            res.header(
               "Access-Control-Allow-Methods",
               "GET, POST, PUT, DELETE, PATCH"
            );
         next();
      });
   }

   start() {
      this.app.listen(this.port, async () => {
         console.log(
            `Servidor corriendo exitosamente en el puerto ${this.port}`
         );
         try {
            process.env.MONGO_URL &&
               (await connect(process.env.MONGO_URL, {
                  useNewUrlParser: true,
                  useUnifiedTopology: true,
               }));

            console.log("Base de datos sincronizada correctamente");
         } catch (error) {
            console.log("Error al conectarse a la BD", error);
         }
      });
   }
}
