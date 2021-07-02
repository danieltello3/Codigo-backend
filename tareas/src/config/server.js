import express from "express";
import { tareas_router } from "../routes/tareas";
import { json } from "body-parser";

export class Server {
   constructor() {
      this.app = express();
      this.puerto = 8000;
      this.bodyParser();
      this.rutas();
   }
   //metodo para definir las rutas
   rutas() {
      this.app.get("/", (req, res) => {
         res.status(201).send("Bienvenido a mi API");
      });
      this.app.use(tareas_router);
   }
   //forma en la cual configuramos a express para que pueda entender lo que me va a mandar el front
   bodyParser() {
      this.app.use(json());
   }
   //metodo para levantar el servidor
   start() {
      // el metodo listen sirve para levantar el servidor y dejarlo escuchando alguna peticion
      this.app.listen(this.puerto, () => {
         console.log(
            `Servidor corriendo exitosamente en el puerto ${this.puerto}`
         );
      });
   }
}
