import express, { NextFunction, Request, Response } from "express";
import morgan from "morgan";
import { json } from "body-parser";
import { tipoRouter } from "../routes/tipo";
import { accionRouter } from "../routes/accion";
import { usuarioRouter } from "../routes/usuario";
import { productoRouter } from "../routes/producto";
import { imagenRouter } from "../routes/imagen";
import { conexion } from "./sequelize";
import { movimientoRouter } from "../routes/movimiento";
import documentacion from "./swagger.json";
import swaggerUI from "swagger-ui-express";
import dotenv from "dotenv";

dotenv.config();

export default class Server {
   app;
   port = "";
   constructor() {
      this.app = express();
      this.port = process.env.PORT || "8000";
      this.bodyParser();
      this.CORS();
      this.rutas();
   }

   bodyParser() {
      this.app.use(json());
      this.app.use(morgan("dev"));
   }

   CORS() {
      this.app.use((req: Request, res: Response, next: NextFunction) => {
         //indica que origenes(dominios) pueden acceder a mi api
         res.header("Access-Control-Allow-Origin", "*");
         // indica que tipos de cabeceras pueden ser enviadas
         res.header(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization"
         );
         //Indica que metodos pueden acceder a mi backend
         res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
         //si cumple con todo, le damos el pase
         next();
      });
   }

   rutas() {
      this.app.get("/", (req: Request, res: Response) => {
         res.send("Bienvenido a la API de zapateria");
      });
      process.env.NODE_ENV
         ? (documentacion.host = `localhost:${this.port}`)
         : (documentacion.host = `https://zapateria-ts-daniel.herokuapp.com`);
      this.app.use(
         "/docs",
         swaggerUI.serve,
         swaggerUI.setup(documentacion, {
            customCss: ".swagger-ui .topbar { display: none }",
         })
      );
      this.app.use(tipoRouter);
      this.app.use(accionRouter);
      this.app.use(usuarioRouter);
      this.app.use(productoRouter);
      this.app.use(imagenRouter);
      this.app.use(movimientoRouter);
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
