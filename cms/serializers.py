from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from rest_framework import serializers
from os import path


class PlatoSerializer(serializers.ModelSerializer):
    platoFoto = serializers.CharField(max_length=100)

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


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True)
    def save(self):
        usuarioNombre = self.validated_data.get('usuarioNombre')
        usuarioApellido = self.validated_data.get('usuarioApellido')
        usuarioCorreo = self.validated_data.get('usuarioCorreo')
        usuarioTipo = self.validated_data.get('usuarioTipo')
        usuarioTelefono = self.validated_data.get('usuarioTelefono')
        password = self.validated_data.get('password')
        nuevoUsuario = UsuarioModel(
            usuarioNombre=usuarioNombre,
            usuarioApellido=usuarioApellido,
            usuarioCorreo=usuarioCorreo,
            usuarioTipo=usuarioTipo,
            usuarioTelefono=usuarioTelefono
        )
        nuevoUsuario.set_password(password)
        nuevoUsuario.save()
        return nuevoUsuario

    class Meta:
        model = UsuarioModel
        exclude = ['groups', 'user_permissions']
        # es para dar configuracion adicional a los atributos de un model serializer, usando el atributo extra_kwargs se puede editar la configuracion de si solo escritura, solo lectura, required, allow null, default y error messages
        # no es necesari
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class MesasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MesaModel
        fields = '__all__'


class DetalleSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField()
    plato = serializers.IntegerField(
        min_value=1
    )

    def validate(self, data):
        try:
            data['plato'] = PlatoModel.objects.get(platoId=data.get('plato'))
        except:
            raise serializers.ValidationError(detail="el plato no existe")
        if data['plato'].platoCantidad < data.get('cantidad'):
            raise serializers.ValidationError(
                detail="la cantidad es mayor que la disponible")
        return data


class PedidoSerializer(serializers.Serializer):
    documento_cliente = serializers.CharField(
        required=False, min_length=8, max_length=11)
    mesa = serializers.IntegerField(min_value=1)
    detalle = DetalleSerializer(many=True)

    def validate(self, data):
        # validar si la mesa existe en la bd
        try:
            data['mesa'] = MesaModel.objects.get(mesaId=data.get('mesa'))
        except:
            raise serializers.ValidationError(detail='la mesa no existe')

        # validar si hay un documento_cliente y si cumple con la longitud requerida
        documento = data.get('documento_cliente')
        if documento and (len(documento) == 8 or len(documento) == 11):
            return data
        if documento is None:
            return data
        raise serializers.ValidationError(
            detail='El documento debe ser 8 u 11 caracteres')
