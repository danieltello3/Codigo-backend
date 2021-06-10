from flask import Flask, request
from flask_restful import Api
from controllers.usuario import RegistroController
from controllers.movimiento import MovimientosController
from models.sesion import SesionModel
from datetime import timedelta
from os import environ, path
from dotenv import load_dotenv
from config.conexion_bd import base_de_datos
from flask_jwt import JWT
from config.seguridad import autenticador, identificador
from config.custom_jwt import manejo_error_JWT

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'claveSecreta'
# para modificar la fecha de caducidad de la token, su valor x default es 300 segundos
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)
# para modificar el endpoint del login
app.config['JWT_AUTH_URL_RULE'] = '/login'
# modificar el parametro username
app.config['JWT_AUTH_USERNAME_KEY'] = 'correo'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

jsonwebtoken = JWT(app=app, authentication_handler=autenticador,
                   identity_handler=identificador)

jsonwebtoken.jwt_error_callback = manejo_error_JWT

base_de_datos.init_app(app)
# base_de_datos.drop_all(app=app)
base_de_datos.create_all(app=app)

EXTENSIONES_PERMITIDAS = {'pdf', 'png', 'jpg', 'jpeg'}


def archivos_permitidos(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in EXTENSIONES_PERMITIDAS


api = Api(app)


@app.route('/subirArchivo', methods=['POST'])
def subir_archivo():
    print(request.files)
    archivo = request.files['archivo']

    # nombre de archivo
    print(archivo.filename)
    # tipo de archivo
    print(archivo.content_type)
    if archivos_permitidos(archivo.filename):
        archivo.save(path.join("multimedia", archivo.filename))
        return 'ok'
    else:
        return 'archivo no permitido'


api.add_resource(RegistroController, "/registro")
api.add_resource(MovimientosController, "/movimientos")

if __name__ == '__main__':
    app.run(debug=True)
