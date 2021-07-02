import { Sequelize } from "sequelize";
import dotenv from "dotenv";

dotenv.config();

// const conexion = new Sequelize({
//    database: "tareas",
//    username: "username",
//    password: "password",
//    dialect: "mysql",
//    host: "127.0.0.1",
//    port: "3306",
//    timezone: "-05:00",
// });

export const conexion = new Sequelize(process.env.URL_DB, {
   dialect: "mysql",
   timezone: "-05:00",
});
