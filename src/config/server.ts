import express, { Request, Response } from "express";
import morgan from "morgan";
import { json } from "body-parser";
import { tipoRouter } from "../routes/tipo";
import { accionRouter } from "../routes/accion";
import { usuarioRouter } from "../routes/usuario";
import { productoRouter } from "../routes/producto";
import { conexion } from "./sequelize";

export default class Server {
   app;
   port = "";
   constructor() {
      this.app = express();
      this.port = process.env.PORT || "8000";
      this.bodyParser();
      this.rutas();
   }

   bodyParser() {
      this.app.use(json());
      this.app.use(morgan("dev"));
   }

   rutas() {
      this.app.get("/", (req: Request, res: Response) => {
         res.send("Bienvenido a la API de zapateria");
      });
      this.app.use(tipoRouter);
      this.app.use(accionRouter);
      this.app.use(usuarioRouter);
      this.app.use(productoRouter);
   }

   start() {
      this.app.listen(this.port, async () => {
         console.log("Servidor corriendo exitosamente");
         try {
            await conexion.sync();
            console.log("Base de datos sincronizada");
         } catch (error) {
            console.error(error);
         }
      });
   }
}

//para resetear la base de datos poner: conexion.sync({force: true})
