import { model, Schema } from "mongoose";

interface IProducto {
   productoNombre: string;
   productoPrecio: number;
   productoImagen?: string;
   productoTipo?: string;
   detalles?: Array<string>;
}

const productoSchema = new Schema<IProducto>({
   productoNombre: {
      type: Schema.Types.String,
      required: true,
      alias: "nombre",
      maxLength: 40,
   },
   productoPrecio: {
      type: Schema.Types.Decimal128,
      required: true,
      alias: "precio",
   },
   productoImagen: {
      type: Schema.Types.String,
      alias: "imagen",
      default: "default.png",
   },
   productoTipo: {
      type: Schema.Types.String,
      alias: "tipo",
      enum: ["LATTES", "COMIDA", "MERCHANDISING", "FRAPPS"],
   },
   detalles: {
      type: [Schema.Types.ObjectId],
   },
});

export const Producto = model<IProducto>("productos", productoSchema);
