import {Sequelize} from 'sequelize';
import dotenv from 'dotenv';

dotenv.config()

export const conexion = new Sequelize(String(process.env.DATABASE_URL), {
    dialect: "postgres",
    timezone: "-05:00",
    //true, activa los querys sql en la consola
    logging: false
})