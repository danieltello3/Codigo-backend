import { DataTypes } from "sequelize";
import {conexion} from '../config/sequelize'

export default () => conexion.define("producto", {
    productoId: {
        primaryKey: true,
        type: DataTypes.INTEGER,
        autoIncrement: true,
        unique: true,
        field: 'id'
    },
    productoNombre: {
        type: DataTypes.STRING(35),
        allowNull: false,
        field: 'nombre'
    },
    productoPrecio: {
        type: DataTypes.DECIMAL(5,2),
        field: 'precio',
        allowNull: false,
        validate: {
            isFloat: true,
            validacionPersonalizada(valor: Number){
                if(valor < 0){
                    throw new Error('El precio no puede ser negativo')
                }
            }
        },
    },
    productoEstado: {
        type: DataTypes.BOOLEAN,
        defaultValue: true,
        field: 'estado'
    },
    productoImagen: {
        type: DataTypes.TEXT,
        field: 'imagen',
        defaultValue: 'https://loremflickr.com/500/500'
    },
    productoDescripcion: {
        type: DataTypes.STRING(45),
        field: 'descripcion'
    },
},
{
    tableName: 'productos',
    timestamps: false,
})