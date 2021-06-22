from datetime import date
from rest_framework import serializers
from django.utils.timezone import now
from .models import LibroModel, PrestamoModel, UsuarioModel
from django.db import transaction


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
        required=True, help_text="ingrese la fecha de inicio",
        min_value=1990,
        max_value=now().year,
        error_messages={
            'invalid': 'Tipo de dato incorrecto, se esperaba un int pero se mando un string', 'required': 'Falta el inicio'
        })
    fin = serializers.IntegerField(
        required=True, help_text="Ingrese una fecha de fin valida",
        min_value=1990,
        max_value=now().year,
        error_messages={
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


class PrestamoSerializer(serializers.ModelSerializer):
    # def validate(self, data):
    #     # mover las siguientes validaciones al metodo validate
    #     # validar si el usuario no tiene un prestamo activo
    #     # validar si el libro no fue inhabilitado (deleteAt)
    #     # no usar el self.validated_data sino el self.initial_data pero el initial_data no hace la busqueda del libro ni del usuario
    #     # return data
    #     pass

    def save(self):
        prestamoActivo: PrestamoModel = PrestamoModel.objects.filter(
            usuario=self.validated_data.get('usuario').usuarioId, prestamoEstado=True).first()
        libro: LibroModel = self.validated_data.get('libro')
        if prestamoActivo:
            return "El usuario tiene un prestamos activo"
        if libro.deletedAt:
            return "El libro no esta disponible"
        if libro.libroCantidad > 0 and libro.deletedAt is None:
            try:
                with transaction.atomic():
                    libro.libroCantidad = libro.libroCantidad - 1
                    libro.save()
                    nuevoPrestamo = PrestamoModel(
                        prestamoFechaInicio=self.validated_data.get(
                            'prestamoFechaInicio', date.today()),
                        prestamoFechaFin=self.validated_data.get(
                            'prestamoFechaFin'),
                        prestamoEstado=self.validated_data.get(
                            'prestamoEstado', True),
                        usuario=self.validated_data.get('usuario'),
                        libro=self.validated_data.get('libro'),
                    )
                    nuevoPrestamo.save()
                    return nuevoPrestamo
            except Exception as error:
                print(error)
                return error
        else:
            return 'El libro no tiene suficiente unidades'

    class Meta:
        model = PrestamoModel
        fields = '__all__'
