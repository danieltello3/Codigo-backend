from controllers.postre import PostresController
from flask import Flask, request
from flask_restful import Api
from dotenv import load_dotenv
from os import environ
from config.conexion_bd import base_de_datos
from models.postre import PostreModel
from models.preparacion import PreparacionModel
from models.ingrediente import IngredienteModel
from models.receta import RecetaModel

load_dotenv()

app = Flask(__name__)
api = Api(app)
# dialect://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
# si se establece en TRUE, Flask-SQLAlchemy rastreara las modificaciones de los objetos y lanzara señales. su valor predeterminado es None, igual habilita el tracking pero emite una advertencia que se deshabilitara de manera prederminada en futuras versiones. esto consume memoria adicional y si no se va a utilzar es mejor desactivarlo (false)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
base_de_datos.init_app(app)

# base_de_datos.drop_all(app=app)       para eliminar las tablas
# crea todas las tablas defininads en los modelos del proyecto
base_de_datos.create_all(app=app)

app.route("/")


def initial_controller():
    return {
        "message": "Bienvenido a mi API de recetas de postres 🎂"
    }


# defino las rutas usando Flask restful
api.add_resource(PostresController, "/postres")


if __name__ == '__main__':
    app.run(debug=True)
