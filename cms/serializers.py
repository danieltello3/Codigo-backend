from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from rest_framework import serializers
from os import path


class PlatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatoModel
        fields = '__all__'


class ArchivoSerializer(serializers.Serializer):
    archivo = serializers.ImageField(max_length=50, use_url=True)

    def save(self):
        archivo: InMemoryUploadedFile = self.validated_data.get('archivo')
        # para ver el tipo de archivo que es
        print(archivo.content_type)
        # para ver el nombre del archivo
        print(archivo.name)
        # para ver el tamaño del archivo en bytes
        print(archivo.size)
        # archivo.read() -> una vez que se lee el archivo se elimina su informacion
        ruta = default_storage.save(archivo.name, ContentFile(archivo.read()))
        ruta_final = path.join(settings.MEDIA_ROOT, ruta)
        print(ruta_final)
        return settings.MEDIA_URL + ruta


class EliminarArchivoSerializer(serializers.Serializer):
    nombre = serializers.CharField(
        required=True,
        help_text="ingrese nombre del archivo"
    )


class CustomPayloadSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: UsuarioModel):
        token = super(CustomPayloadSerializer, cls).get_token(user)
        print(token)
        token['usuarioTipo'] = user.usuarioTipo
        token['message'] = 'Holis'
        return token
