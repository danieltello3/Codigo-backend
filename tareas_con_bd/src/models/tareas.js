import { conexion } from "../config/sequelize";
import { DataTypes } from "sequelize";

export const tareaModel = () =>
   conexion.define(
      "tarea",
      {
         tareaId: {
            primaryKey: true,
            unique: true,
            autoIncrement: true,
            allowNull: false,
            field: "id",
            type: DataTypes.INTEGER,
         },
         tareaNombre: {
            type: DataTypes.STRING(50),
            field: "nombre",
            allowNull: false,
         },
         tareaEstado: {
            type: DataTypes.BOOLEAN,
            field: "estado",
            defaultValue: false,
         },
      },
      {
         tableName: "tareas",
         timestamps: true,
         updatedAt: "fecha_actualizacion",
      }
   );
