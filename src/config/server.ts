import express, {Request, Response} from 'express'
import { json } from 'body-parser';
import { conexion } from './sequelize';

export default class Server {
    app;
    port = '';
    constructor(){
        this.app = express();
        this.port = process.env.PORT || '8000'
        this.bodyParser()
        this.rutas()
    }

    bodyParser(){
        this.app.use(json())
    }
    
    rutas(){
        this.app.get('/',(req: Request,res: Response)=>{
            res.send('Bienvenido a la API de zapateria');
        })
    }
    
    start(){
        this.app.listen(this.port,async ()=>{
            console.log("Servidor corriendo exitosamente")
            try{
                await conexion.sync();
                console.log('Base de datos sincronizada');
            }catch(error){
                console.error(error)
            }
        })
    }
}