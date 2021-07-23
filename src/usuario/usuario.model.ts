import { model, Schema } from "mongoose";
import { hashSync } from "bcrypt";

interface IDireccion {
   zip?: string;
   calle?: string;
   numero?: number;
}

interface IUsuario {
   usuarioCorreo: string;
   usuarioNombre: string;
   usuarioApellido: string;
   usuarioTelefono?: string;
   usuarioDni: string;
   usuarioDireccion?: IDireccion;
   usuarioPassword?: string;
   usuarioTipo: string;
}

const direccionSchema = new Schema<IDireccion>(
   {
      zip: Schema.Types.String,
      calle: Schema.Types.String,
      numero: Schema.Types.Number,
   },
   {
      _id: false,
      timestamps: false,
   }
);

const usuarioSchema = new Schema<IUsuario>(
   {
      usuarioCorreo: {
         type: Schema.Types.String,
         alias: "correo",
         required: true,
         index: true,
         unique: true,
      },
      usuarioNombre: {
         type: Schema.Types.String,
         alias: "nombre",
         required: true,
      },
      usuarioApellido: {
         type: Schema.Types.String,
         alias: "apellido",
      },
      usuarioTelefono: {
         type: Schema.Types.String,
         alias: "telefono",
      },
      usuarioDni: {
         type: Schema.Types.String,
         required: true,
         alias: "dni",
         index: true,
         unique: true,
      },
      usuarioDireccion: {
         type: direccionSchema,
         alias: "direccion",
      },
      usuarioPassword: {
         type: Schema.Types.String,
         set: (valor: string) => hashSync(valor, 10),
         alias: "password",
         required: true,
      },
      usuarioTipo: {
         type: Schema.Types.String,
         alias: "tipo",
         enum: ["CLIENTE", "PERSONAL"],
         required: true,
      },
   },
   { timestamps: { createdAt: "fecha_creacion", updatedAt: false } }
);

export const Usuario = model<IUsuario>("usuarios", usuarioSchema);
