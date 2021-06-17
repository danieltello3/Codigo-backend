from .models import LibroModel
from rest_framework import serializers


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        # model => definir en que modelo se basara para la serializacion
        model = LibroModel
        # field => indica que campos seran necesarios para el funcionamiento de este serializer
        fields = '__all__'
        # fields => si queremos usar algunas columnas se define en listas o tuplas
        # fields = ['col1'] || fields = ('col1')
        #exclude= ['libroId']
        # no se puede usar fields y exclude a la vez.
