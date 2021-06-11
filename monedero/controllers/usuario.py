from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel
from re import fullmatch, search
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
from os import environ
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

load_dotenv()


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
        patron_correo = '^[a-zA-Z0-9._-]+[@]\w+[.]\w{2,3}$'
        print(search(patron_correo, correo))
        patron_password = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#&?])[a-zA-Z\d@$!%*#&?]{6,}$'
        print(fullmatch(patron_password, password))
        if search(patron_correo, correo):
            try:
                nuevoUsuario = UsuarioModel(nombre, apellido, correo, password)
                # nuevoUsuario.save()
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
        # return {
        #     "message": "Usuario no encontrado",
        #     "content": None,
        #     "success": False
        # }, 404

        # TODO : VALIDAR QUE ES UN CORREO VALIDO Y LUEGO BUSCAR SI EXISTE EL USUARIO CON ESE CORREO, SINO EXISTE NO PROCEDER Y RETORNAR EL MENSAJE QUE NO EXISTE.
        # ----------------------------------------------
        # YOUR CODE HERE
        # ----------------------------------------------
        # secret_key = Fernet.generate_key()
        # inicio mi objeto Fernet con la clave definida en mi variable de entorno
        fernet = Fernet(environ.get("FERNET_SECRET"))
        # creo un payload que sera lo que mandare por el correo indicando la fecha de caducidad, y el correo
        payload = {
            "fecha_caducidad": str(datetime.now() + timedelta(minutes=30)),
            "correo": correo
        }
        print(payload)
        # el metodo dumps convierte un diccionario a un json
        payload_json = json.dumps(payload)
        token = fernet.encrypt(bytes(payload_json, 'utf-8'))
        print(token)
        return 'ok'
