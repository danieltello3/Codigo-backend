from models.postre import PostreModel
from flask_restful import Resource, reqparse
from models.preparacion import PreparacionModel
from config.conexion_bd import base_de_datos

serializerPreparacion = reqparse.RequestParser(bundle_errors=True)

serializerPreparacion.add_argument(
    'orden',
    type=int,
    required=True,
    help='falta el orden',
    location='json'
)
serializerPreparacion.add_argument(
    'descripcion',
    type=str,
    required=True,
    help='falta la descripcion',
    location='json'

)
serializerPreparacion.add_argument(
    'postre_id',
    type=int,
    required=True,
    help='falta el postre_id',
    location='json'
)


def validarPostre(postre_id):
    return base_de_datos.session.query(PostreModel).filter_by(postreID=postre_id).first()


class PreparacionesController(Resource):
    def post(self):
        data = serializerPreparacion.parse_args()
        nuevaPreparacion = PreparacionModel(data.get('orden'), data.get(
            'descripcion'), data.get('postre_id'))
        if validarPostre(postre_id=data.get('postre_id')):
            if base_de_datos.session.query(PreparacionModel).filter_by(postre=data.get('postre_id'), preparacionOrden=data.get('orden')).first():
                return {
                    "success": False,
                    "content": None,
                    "message": f"este numero de orden {data.get('orden')} para el postre {data.get('postre_id')} ya existe"
                }, 400
            else:
                # print(data.get('orden'))
                print(base_de_datos.session.query(PreparacionModel).order_by(
                    PreparacionModel.preparacionOrden.desc()).first().preparacionOrden)
                if base_de_datos.session.query(PreparacionModel).order_by(PreparacionModel.preparacionOrden.desc()).first().preparacionOrden == data.get('orden') - 1:
                    nuevaPreparacion.save()
                    return{
                        "success": True,
                        "content": nuevaPreparacion.json(),
                        "message": "Preparacion creada exitosamente"
                    }, 201
                else:
                    return {
                        "success": False,
                        "content": None,
                        "message": "el orden debe ser correlativo"
                    }

        else:
            return {
                "success": False,
                "content": None,
                "message": "postre no existe"
            }, 400

    def get(self):
        pass
