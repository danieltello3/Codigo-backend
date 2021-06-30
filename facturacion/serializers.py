from django.db.models import fields
from facturacion.models import ComprobanteModel
from cms.models import PedidosModel
from rest_framework import serializers


class ComprobanteSerializer(serializers.Serializer):
    pedidoId = serializers.IntegerField()
    #tipoComprobante = serializers.IntegerField(min_value=1, max_value=2)
    tipoComprobante = serializers.ChoiceField(choices=[1, 2])
    observaciones = serializers.CharField(max_length=1000, required=False)

    def validate(self, data):
        try:
            data['pedidoId'] = PedidosModel.objects.get(
                pedidoId=data.get('pedidoId'))
            return data
        except:
            raise serializers.ValidationError(detail="el pedido no existe")


class ComprobanteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComprobanteModel
        fields = '__all__'
