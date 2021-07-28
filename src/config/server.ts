import express, { Express } from "express";
import { Server as SocketIO } from "socket.io";
import { createServer, Server as HTTPServer } from "http";
import { Request, Response } from "express-serve-static-core";

interface IRegistro {
   username: string;
}

interface IUsuario extends IRegistro {
   id: string;
}

interface IMensaje {
   username: string;
   mensaje: string;
   fecha: Date;
}

export default class Server {
   app: Express;
   port: string | number;
   httpServer: HTTPServer;
   io: SocketIO;
   constructor() {
      this.app = express();
      this.port = process.env.PORT || 8000;
      this.httpServer = createServer(this.app);
      this.io = new SocketIO(this.httpServer, {
         cors: { origin: "*" },
      });
      this.rutas();
      this.escucharSockets();
   }

   rutas() {
      this.app.get("/", (req: Request, res: Response) => {
         res.json({
            success: true,
            message: "yo soy la respuesta desde un controlador REST",
         });
      });
   }

   escucharSockets() {
      //el metodo on se ejecuta cuando el cliente envie un evento
      //nosotors podemos crear los eventos que querramos, pero hay metodos ya creados que no se pueden modificar
      let usuarios: Array<IUsuario> = [];
      const mensajes: Array<IMensaje> = [];
      this.io.on("connect", (cliente) => {
         console.log(`se conecto el cliente! ${cliente.id}`);
         cliente.on("registrar", (objCliente: IRegistro) => {
            const usuarioEncontrado = usuarios.filter(
               (usuario) => usuario.id === cliente.id
            )[0];
            if (!usuarioEncontrado) {
               usuarios.push({
                  username: objCliente.username,
                  id: cliente.id,
               });
               console.log(usuarios);
               this.io.emit("lista-usuarios", usuarios);
            }
         });

         cliente.on("mensaje-nuevo", (mensaje: string) => {
            const { username } = usuarios.filter(
               (usuario) => usuario.id === cliente.id
            )[0];
            mensajes.push({
               mensaje,
               username,
               fecha: new Date(),
            });
            this.io.emit("lista-mensajes", mensajes);
            console.log(mensajes);
         });
         cliente.on("disconnect", (reason) => {
            console.log(reason);
            // usuarios.splice(
            //    usuarios.findIndex((usuario) => usuario.id === cliente.id),
            //    1
            // );
            usuarios = usuarios.filter((usuario) => usuario.id !== cliente.id);

            console.log(`se desconecto el usuario ${cliente.id}`);
            //this.io.emit, hacemos un broadcast enviando el evento a todos los usuarios conectados
            this.io.emit("lista-usuarios", usuarios);
            console.log(usuarios);
         });
         //si nosotros queremos hacer la emision de un evento pero solamente al usuario que la ha solicitado, entonces se relizara mediante cliente
         cliente.emit("lista-usuarios", usuarios);
         cliente.emit("lista-mensajes", mensajes);
         //si queremos emitir un evento a todos los demas usuarios excepto al usuario conectado, entonces haremos un broadcast
         //cliente.broadcast.emit("lista-usuarios",usuarios)
      });
   }

   start() {
      this.httpServer.listen(this.port, () => {
         console.log("Servidor corriendo exitosamente");
      });
   }
}
