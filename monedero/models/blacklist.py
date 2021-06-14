from datetime import datetime
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types


class BlacklistModel(base_de_datos.Model):
    __tablename__ = 'blacklists'

    blacklistId = Column(name='id', type_=types.Integer, primary_key=True,
                         unique=True, autoincrement=True, nullable=False)
    blacklistToken = Column(name='token', type_=types.Text, nullable=False)
    blacklistTime = Column(name='fecha', type_=types.DateTime, nullable=False)

    def __init__(self, token):
        self.blacklistToken = token
        self.blacklistTime = datetime.now()

    def save(self):
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    def json(self):
        return {
            "blacklistToken": self.blacklistToken,
            "blacklistTime": self.blacklistTime,
        }
