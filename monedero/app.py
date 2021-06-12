from flask import Flask, request, send_file, render_template
from flask_restful import Api
from controllers.usuario import RegistroController, ForgotPasswordController, ResetPasswordController
from controllers.movimiento import MovimientosController
from models.sesion import SesionModel
from datetime import timedelta, datetime
from os import environ, path, remove
from dotenv import load_dotenv
from config.conexion_bd import base_de_datos
from flask_jwt import JWT
from config.seguridad import autenticador, identificador
from config.custom_jwt import manejo_error_JWT
# sirve para validar el nombre del archivo, antes de guardarlo
from werkzeug.utils import secure_filename
from uuid import uuid4
from flask_cors import CORS
from cryptography.fernet import Fernet
import json


load_dotenv()

UPLOAD_FOLDER = 'multimedia'
app = Flask(__name__)
CORS(app=app,
     methods=['GET', 'POST'], allow_headers=['*'])
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get("JWT_SECRET")
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

        # primero saco el formato del archivo
        formato_archivo = archivo.filename.rsplit(".", 1)[-1]
        nombre_archivo = str(uuid4())+'.'+formato_archivo
        nombre_archivo = secure_filename(nombre_archivo)
        archivo.save(path.join(UPLOAD_FOLDER, nombre_archivo))
        return {
            "success": True,
            "content": request.host_url+'media/'+nombre_archivo,
            "message": "archivo registrado exitosamente"
        }
    else:
        return {
            "success": False,
            "content": None,
            "message": "archivo no permitido"
        }, 400


@app.route("/media/<string:nombre>", methods=['GET'])
def devolver_archivo(nombre):
    try:
        return send_file(path.join(UPLOAD_FOLDER, nombre))
    except:
        return send_file(path.join(UPLOAD_FOLDER, "not_found.png")), 404


@app.route("/eliminarArchivo/<string:nombre>", methods=['DELETE'])
def eliminar_archivo(nombre):
    try:
        remove(path.join(UPLOAD_FOLDER, nombre))
        return {
            "success": True,
            "content": None,
            "message": "archivo eliminado exitosamente"
        }
    except:
        return {
            "success": False,
            "content": None,
            "message": "archivo eliminado exitosamente"
        }, 404


@app.route('/', methods=['GET'])
def inicio():
    return render_template('index.jinja', mensaje='Hola amigos como estan?')


@app.route('/recuperarPassword/<string:token>')
def recuperar_password(token):
    fernet = Fernet(environ.get("FERNET_SECRET"))
    # decrypt(b'token')
    # el metodo decrypt recibe una token pero en formato de bytes y luego si es que cumple con la password devolvera el mensaje encriptado pero en bytes, y para convertirlo en string usamos el metodo decode
    try:
        respuesta = fernet.decrypt(bytes(token, 'utf-8')).decode('utf-8')
        respuesta_diccionario = json.loads(respuesta)
        fecha_caducidad = datetime.strptime(
            respuesta_diccionario['fecha_caducidad'], '%Y-%m-%d %H:%M:%S.%f')

        if fecha_caducidad > datetime.now():
            return render_template('recovery_password.jinja', correo=respuesta_diccionario['correo'])
        else:
            return render_template('bad_token.jinja')

    except:
        return render_template('bad_token.jinja')


api.add_resource(RegistroController, "/registro")
api.add_resource(MovimientosController, "/movimientos")
api.add_resource(ForgotPasswordController, "/olvide-password")
api.add_resource(ResetPasswordController, "/reset-password")

if __name__ == '__main__':
    app.run(debug=True)
