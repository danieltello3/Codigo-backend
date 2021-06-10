from flask_restful import Resource, reqparse
from models.movimiento import MovimientoModel
from datetime import datetime
from flask_jwt import jwt_required


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
        type=datetime,
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
        data = self.serializer.parse_args()
        print(data)
        return 'ok'

    def get(self):
        pass
