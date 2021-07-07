import { DataTypes } from "sequelize";
import { conexion } from "./sequelize";

const productoModel = () =>
   conexion.define(
      "producto",
      {
         productoId: {
            primaryKey: true,
            type: DataTypes.INTEGER,
            autoIncrement: true,
            unique: true,
            field: "id",
         },
         productoNombre: {
            type: DataTypes.STRING(35),
            allowNull: false,
            field: "nombre",
         },
         productoPrecio: {
            type: DataTypes.DECIMAL(5, 2),
            field: "precio",
            allowNull: false,
            validate: {
               isFloat: true,
               validacionPersonalizada(valor: Number) {
                  if (valor < 0) {
                     throw new Error("El precio no puede ser negativo");
                  }
               },
            },
         },
         productoEstado: {
            type: DataTypes.BOOLEAN,
            defaultValue: true,
            field: "estado",
         },
         productoImagen: {
            type: DataTypes.TEXT,
            field: "imagen",
            defaultValue: "https://loremflickr.com/500/500",
         },
         productoDescripcion: {
            type: DataTypes.STRING(45),
            field: "descripcion",
         },
      },
      {
         tableName: "productos",
         timestamps: false,
      }
   );

const tipoModel = () =>
   conexion.define(
      "tipo",
      {
         tipoId: {
            type: DataTypes.INTEGER,
            field: "id",
            autoIncrement: true,
            primaryKey: true,
            unique: true,
         },
         tipoDescripcion: {
            type: DataTypes.STRING(45),
            field: "descripcion",
            unique: true,
         },
      },
      {
         tableName: "tipos",
         timestamps: false,
      }
   );

const accionModel = () =>
   conexion.define(
      "accion",
      {
         accionId: {
            type: DataTypes.INTEGER,
            field: "id",
            autoIncrement: true,
            primaryKey: true,
            unique: true,
         },
         accionDescripcion: {
            type: DataTypes.STRING(45),
            field: "descripcion",
         },
      },
      {
         tableName: "acciones",
         timestamps: false,
      }
   );

const usuarioModel = () =>
   conexion.define(
      "usuario",
      {
         usuarioId: {
            type: DataTypes.INTEGER,
            field: "id",
            primaryKey: true,
            autoIncrement: true,
            unique: true,
         },
         usuarioNombre: {
            type: DataTypes.STRING(45),
            field: "nombre",
            allowNull: false,
            validate: {
               is: /([a-zA-Z])\w+([ ])/,
            },
         },
         usuarioCorreo: {
            type: DataTypes.STRING(35),
            field: "correo",
            allowNull: false,
            validate: {
               isEmail: true,
            },
         },
         usuarioPassword: {
            type: DataTypes.TEXT,
            field: "password",
            allowNull: false,
            validate: {
               isAlpha: true,
            },
         },
         usuarioImagen: {
            type: DataTypes.TEXT,
            field: "imagen",
            allowNull: false,
            validate: {
               isUrl: true,
            },
         },
      },
      {
         tableName: "usuarios",
         timestamps: false,
      }
   );

const movimientoModel = () =>
   conexion.define(
      "movimiento",
      {
         movimientoId: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            unique: true,
            autoIncrement: true,
            field: "id",
         },
         movimientoFecha: {
            type: DataTypes.DATE,
            defaultValue: new Date(),
            field: "fecha",
            allowNull: false,
         },
         movimientoTipo: {
            type: DataTypes.STRING(20),
            field: "tipo",
            allowNull: false,
            validate: {
               isIn: [["ingreso", "egreso"]],
            },
         },
         movimientoTotal: {
            type: DataTypes.DECIMAL(5, 2),
            field: "total",
            allowNull: false,
         },
      },
      {
         tableName: "movimientos",
         timestamps: false,
      }
   );

const detalleMovimientoModel = () =>
   conexion.define(
      "detalleMovimiento",
      {
         detalleMovientoId: {
            field: "id",
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true,
            unique: true,
         },
         detalleMovimientoCantidad: {
            type: DataTypes.INTEGER,
            allowNull: false,
            field: "cantidad",
         },
         detalleMovimientoPrecio: {
            field: "precio",
            type: DataTypes.DECIMAL(5, 2),
         },
      },
      {
         tableName: "detalle_movimientos",
         timestamps: false,
      }
   );

// RELACIONES

export const Producto = productoModel();
export const Tipo = tipoModel();
export const Accion = accionModel();
export const Usuario = usuarioModel();
export const Movimiento = movimientoModel();
export const DetalleMovimiento = detalleMovimientoModel();

Producto.hasMany(DetalleMovimiento, { foreignKey: "producto_id" });
DetalleMovimiento.belongsTo(Producto, { foreignKey: "producto_id" });

Tipo.hasMany(Accion, { foreignKey: { name: "tipo_id", allowNull: false } });
Accion.belongsTo(Tipo, { foreignKey: { name: "tipo_id", allowNull: false } });

Tipo.hasMany(Usuario, { foreignKey: "tipo_id" });
Usuario.belongsTo(Tipo, { foreignKey: "tipo_id" });

Usuario.hasMany(Movimiento, { foreignKey: "usuario_id" });
Movimiento.belongsTo(Usuario, { foreignKey: "usuario_id" });

Movimiento.hasMany(DetalleMovimiento, { foreignKey: "movimiento_id" });
DetalleMovimiento.belongsTo(Movimiento, { foreignKey: "movimiento_id" });
