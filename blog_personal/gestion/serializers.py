from rest_framework import serializers
from django.utils.timezone import now
from .models import LibroModel, UsuarioModel


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        # model => definir en que modelo se basara para la serializacion
        model = LibroModel
        # field => indica que campos seran necesarios para el funcionamiento de este serializer
        #fields = '__all__'

        # fields => si queremos usar algunas columnas se define en listas o tuplas
        # fields = ['col1'] || fields = ('col1')
        exclude = ['deletedAt']
        # no se puede usar fields y exclude a la vez.


class BusquedaLibroSerializer(serializers.Serializer):
    inicio = serializers.IntegerField(
        required=True, help_text="ingrese la fecha de inicio", min_value=1990, max_value=now().year,
        error_messages={
            'invalid': 'Tipo de dato incorrecto, se esperaba un int pero se mando un string', 'required': 'Falta el inicio'
        })
    fin = serializers.IntegerField(
        required=True, help_text="Ingrese una fecha de fin valida", min_value=1990, max_value=now().year, error_messages={
            'max_value': 'Error el valor maximo es {max_value}',
            'min_value': 'Error el valor minimo es {min_value}'
        })

    def validate(self, data):
        """Metodo que se ejecturara cuando nosotros llamemos al metodo is_valid()"""
        if data.get('inicio') <= data.get('fin'):
            return data
        raise serializers.ValidationError(
            detail='inicio debe ser menor que fin')


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioModel
        fields = '__all__'
