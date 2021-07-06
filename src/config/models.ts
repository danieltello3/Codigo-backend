import { DataTypes } from "sequelize";
import {conexion} from './sequelize'

export const productoModel = () => conexion.define("producto", {
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

export const tipoModel = ()=> conexion.define('tipo', {
    tipoId: {
        type: DataTypes.INTEGER,
        field: 'id',
        primaryKey: true,
        unique: true,
    },
    tipoDescripcion: {
        type: DataTypes.STRING(45),
        field: 'descripcion'
    }
},{
    tableName: 'tipos',
    timestamps: false,
})

export const accionModel = () => conexion.define('accion', {
    accionId: {
        type: DataTypes.INTEGER,
        field: 'id',
        primaryKey: true,
        unique: true,
    },
    accionDescripcion: {
        type: DataTypes.STRING(45),
        field: 'descripcion'
    }
},{
    tableName: 'acciones',
    timestamps: false,
})

const usuarioModel = () => conexion.define('usuario', {
    usuarioId: {
        type: DataTypes.INTEGER,
        field: 'id',
        primaryKey: true,
        unique: true,
    },
    usuarioNombre: {
        type: DataTypes.STRING(45),
        field: 'nombre',
        allowNull: false,
        validate: {
            is: /([a-zA-Z])\w+([ ])/,
        }
    },
    usuarioCorreo: {
        type: DataTypes.STRING(35),
        field: 'correo',
        allowNull: false,
        validate: {
            isEmail: true,
        }
    },
    usuarioPassword: {
        type: DataTypes.TEXT,
        field: 'password',
        allowNull: false,
        validate: {
            isAlpha:true,
        }
    },
    usuarioImagen: {
        type: DataTypes.TEXT,
        field: 'imagen',
        allowNull: false,
        validate: {
            isUrl: true,
        }
    }
},{
    tableName: 'usuarios',
    timestamps: false,
})

const movimientoModel = () => conexion.define('movimiento', {
    movimientoId: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        unique: true,
        field: 'id'
    },
    movimientoFecha: {
        type: DataTypes.DATE,
        defaultValue: new Date(),
        field: 'fecha',
        allowNull: false,
    },
    movimientoTipo: {
        type: DataTypes.STRING(20),
        field: 'tipo',
        allowNull: false,
        validate: {
            isIn: [['ingreso', 'egreso']]
        }
    },
    movimientoTotal: {
        type: DataTypes.DECIMAL(5,2),
        field: 'total',
        allowNull: false,
    }
},{
    tableName: 'movimientos',
    timestamps: false,
})

const detalleMovimientoModel = ()=> conexion.define("detalleMovimiento", {
    detalleMovientoId: {
        field: 'id',
        type: DataTypes.INTEGER,
        primaryKey: true,
        unique: true
    },
    detalleMovimientoCantidad: {
        type: DataTypes.INTEGER,
        allowNull: false,
        field: 'cantidad'
    },
    detalleMovimientoPrecio: {
        field: 'precio',
        type: DataTypes.DECIMAL(5,2)
    }
},{
    tableName: 'detalle_movimientos',
    timestamps: false,
})