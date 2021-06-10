from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel
from re import fullmatch, search
from sqlalchemy.exc import IntegrityError


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
