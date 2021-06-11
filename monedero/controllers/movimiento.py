from flask_restful import Resource, reqparse
from models.movimiento import MovimientoModel
from datetime import datetime
from flask_jwt import jwt_required, current_identity


class MovimientosController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument(
        'nombre',
        type=str,
        required=True,
        help='Falta el nombre',
        location='json'
    )
    serializer.add_argument(
        'monto',
        type=float,
        required=True,
        help='Falta el monto',
        location='json'
    )
    serializer.add_argument(
        'fecha',
        type=str,
        required=False,
        help='Falta la fecha',
        location='json'
    )
    serializer.add_argument(
        'imagen',
        type=str,
        required=False,
        help='Falta la imagen',
        location='json'
    )
    serializer.add_argument(
        'tipo',
        type=str,
        required=True,
        help='Falta el tipo',
        choices=('egreso', 'ingreso'),
        location='json'
    )
    # con el decorador jwt_required estoy indicando que este metodo de esta clase tiene que recibir una token (es protegida)

    @jwt_required()
    def post(self):
        print(current_identity)
        data = self.serializer.parse_args()
        print(data)
        # strptime => convierte de un string a una fecha mediante formato
        # strftime => convierte una fecha a un string
        try:
            fecha = datetime.strptime(data['fecha'], '%Y-%m-%d %H:%M:%S')
            #fecha_en_texto = fecha.strftime('%Y-%m-%d %H:%M:%S')
            # # print(type(fecha))
            nuevoMovimiento = MovimientoModel(data['nombre'], data['monto'], fecha,
                                              data['imagen'], data['tipo'], current_identity.get('usuarioID'))
            nuevoMovimiento.save()

            return {
                "success": True,
                "content": nuevoMovimiento.json(),
                "message": "movimiento registrado exitosamente"
            }
        except:
            return {
                "success": False,
                "message": "Formato de fecha incorrecto, el formato es YYYY-MM-DD HH:MM:SS",
                "content": None
            }

    def get(self):
        pass
