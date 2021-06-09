from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types, orm
import bcrypt


class UsuarioModel(base_de_datos.Model):
    __tablename__ = "usuarios"

    usuarioId = Column(name='id', type_=types.Integer, primary_key=True,
                       unique=True, autoincrement=True, nullable=False)
    usuarioNombre = Column(
        name='nombre', type_=types.String(45), nullable=False)
    usuarioApellido = Column(
        name='apellido', type_=types.String(45), nullable=False)
    usuarioCorreo = Column(
        name='correo', type_=types.String(25), nullable=False, unique=True)
    usuarioPassword = Column(name='password', type_=types.TEXT, nullable=False)

    movimientos = orm.relationship(
        'MovimientoModel', backref='movimientoUsuario')

    def __init__(self, nombre, apellido, correo, password):
        self.usuarioNombre = nombre
        self.usuarioCorreo = correo
        self.usuarioApellido = apellido
        # Encriptar contraseña
        # primero se convierte en bytes mediante el formato de escritura utf-8
        passwordBytes = bytes(password, "utf-8")
        # el metodo hashpw agarra la password y un salt generado aleatoriamente para fusionarlos y luego devolver la password haseada
        passwordHash = bcrypt.hashpw(passwordBytes, bcrypt.gensalt())
        # el metodo decode convierte el tipo de dato bytes a string
        passwordString = passwordHash.decode("utf-8")
        self.usuarioPassword = passwordString

    def save(self):
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    def json(self):
        return {
            "usuarioID": self.usuarioId,
            "usuarioNombre": self.usuarioNombre,
            "usuarioApellido": self.usuarioApellido,
            "usuarioCorreo": self.usuarioCorreo
        }
