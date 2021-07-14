import { Sequelize, Options } from "sequelize";
import dotenv from "dotenv";

dotenv.config();

// const opciones: Options = {
//     dialect: "postgres",
//    timezone: "-05:00",
//    //true, activa los querys sql en la consola
//    logging: false,
//    ssl: true,
// }

export const conexion = new Sequelize(String(process.env.DATABASE_URL), {
   dialect: "postgres",
   dialectOptions:
      process.env.NODE_ENV != "production"
         ? {}
         : {
              ssl: {
                 rejectUnauthorized: false,
              },
           },
   timezone: "-05:00",
   //true, activa los querys sql en la consola
   logging: false,
});
