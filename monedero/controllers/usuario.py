import bcrypt
from flask_restful import Resource, reqparse, request
from models.usuario import UsuarioModel
from re import fullmatch, search
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
from os import environ
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
from config.conexion_bd import base_de_datos
from utils.enviar_correo_puro import enviarCorreo


load_dotenv()

PATRON_CORREO = '^[a-zA-Z0-9._-]+[@]\w+[.]\w{2,3}$'
PATRON_PASSWORD = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#&?])[a-zA-Z\d@$!%*#&?]{6,}$'


class RegistroController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument(
        'nombre',
        type=str,
        required=True,
        help="Falta el nombre",
        location='json'
    )
    serializer.add_argument(
        'apellido',
        type=str,
        required=True,
        help="Falta el apellido",
        location='json'
    )
    serializer.add_argument(
        'correo',
        type=str,
        required=True,
        help="Falta el correo",
        location='json'
    )
    serializer.add_argument(
        'password',
        type=str,
        required=True,
        help="Falta el password",
        location='json'
    )

    def post(self):
        data = self.serializer.parse_args()
        # validar si es un correo valido
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        password = data.get('password')
        correo = data.get('correo')
        # [\._]?
        # print(search(PATRON_CORREO, correo))
        # print(fullmatch(PATRON_PASSWORD, password))

        if search(PATRON_CORREO, correo) and fullmatch(PATRON_PASSWORD, password):
            try:
                nuevoUsuario = UsuarioModel(nombre, apellido, correo, password)
                nuevoUsuario.save()
                return {
                    "success": True,
                    "content": nuevoUsuario.json(),
                    "message": "Usuario registrado exitosamente"
                }, 201
            except IntegrityError:
                return {
                    "success": False,
                    "content": None,
                    "message": "correo ya existe"
                }, 400
            except:
                return {
                    "success": False,
                    "content": None,
                    "message": "Error inesperado"
                }, 400
        else:
            return {
                "success": False,
                "content": None,
                "message": "correo o password incorrecto"
            }, 400

        # if "@" in correo and "." in correo:
        #     print("si hay")
        # else:
        #     print("no hay")
        # return 'ok'


class ForgotPasswordController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument(
        'correo',
        type=str,
        required=True,
        location='json',
        help='falta el correo'
    )

    def post(self):
        data = self.serializer.parse_args()
        correo = data['correo']
        # secret_key = Fernet.generate_key()
        # inicio mi objeto Fernet con la clave definida en mi variable de entorno
        fernet = Fernet(environ.get("FERNET_SECRET"))
        if search(PATRON_CORREO, correo):
            usuario = base_de_datos.session.query(
                UsuarioModel).filter_by(usuarioCorreo=correo).first()
            if usuario:
                # creo un payload que sera lo que mandare por el correo indicando la fecha de caducidad, y el correo
                payload = {
                    "fecha_caducidad": str(datetime.now() + timedelta(minutes=30)),
                    "correo": correo
                }
                # print(payload)
                # el metodo dumps convierte un diccionario a un json
                payload_json = json.dumps(payload)
                token = fernet.encrypt(bytes(payload_json, 'utf-8'))
                # print(token)
                link = request.host_url + \
                    'recuperarPassword/'+token.decode('utf-8')
                respuesta = enviarCorreo(usuario.usuarioCorreo,
                                         usuario.usuarioNombre, link)
                if respuesta:
                    return {
                        "success": True,
                        "content": None,
                        "message": "Correo enviado correctamente"
                    }
                else:
                    return {
                        "success": False,
                        "content": None,
                        "message": "Error al enviar el correo, intente nuevamente"
                    }, 500
            else:
                return {
                    "message": "Usuario no encontrado",
                    "content": None,
                    "success": False
                }, 404
        else:
            return {
                "message": "Por favor indicar un correo valido",
                "content": None,
                "success": False
            }, 400


class ResetPasswordController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument(
        'correo',
        type=str,
        required=True,
        location='json',
        help='falta el correo'
    )
    serializer.add_argument(
        'new_password',
        type=str,
        required=True,
        location='json',
        help='falta la password'
    )

    def post(self):
        data = self.serializer.parse_args()
        if search(PATRON_CORREO, data['correo']):
            usuario = base_de_datos.session.query(UsuarioModel).filter_by(
                usuarioCorreo=data.get('correo')).first()
            if usuario:
                if fullmatch(PATRON_PASSWORD, data['new_password']):
                    new_passwordBytes = bytes(data['new_password'], "utf-8")
                    new_passwordHash = bcrypt.hashpw(
                        new_passwordBytes, bcrypt.gensalt())
                    new_passwordString = new_passwordHash.decode("utf-8")
                    usuario.usuarioPassword = new_passwordString
                    usuario.save()
                    return {
                        "success": True,
                        "content": usuario.json(),
                        "message": "Password se actualizo exitosamente"
                    }
                else:
                    return {
                        "success": False,
                        "content": None,
                        "message": "La password debe tener al menos 6 caracteres, una mayuscula, una minuscula, un numero y un caracter especial"
                    }
            else:
                return {
                    "success": False,
                    "content": None,
                    "message": "usuario no encontrado"
                }, 400

        else:
            return {
                "success": False,
                "content": None,
                "message": "Formato de correo incorrecto"
            }
