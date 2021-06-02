from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types, orm


class PostreModel(base_de_datos.Model):
    __tablename__ = "postres"
    postreID = Column(name='id', primary_key=True,
                      autoincrement=True, unique=True, type_=types.Integer)

    postreNombre = Column(name='nombre', type_=types.String(length=45))
    postrePorcion = Column(name='porcion', type_=types.String(length=25))

    # el relationship sirve para indicar todos los hijos que puede tener ese modelo (todas sus FK) que puedan existir en determinado modelo
    # el backref creara un atributo virtual en el model del hijo (preparacion) para que pueda acceder a todo el objeto de PostreModel sin la necesidad de hacer una sub consulta (creara un join cuando sea necesario)
    # lazy => define cuando sqlAlchemy va a cargar la data adyacente de la base de datos
    preparaciones = orm.relationship(
        'PreparacionModel', backref='preparacionPostre', lazy=True)

    recetas = orm.relationship('RecetaModel', backref='recetaPostre')

    def __init__(self, nombre, porcion):
        self.postreNombre = nombre
        self.postrePorcion = porcion
