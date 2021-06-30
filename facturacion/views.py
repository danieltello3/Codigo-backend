from facturacion.models import ComprobanteModel
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from facturacion.serializers import ComprobanteModelSerializer, ComprobanteSerializer
from .generarComprobante import crearComprobante


class ComprobanteController(CreateAPIView):
    serializer_class = ComprobanteSerializer

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if ComprobanteModel.objects.get(pedido=request.data.get('pedidoId')):
            return Response(data={
                "success": False,
                "content": None,
                "message": "El pedido ya tiene un comprobante"
            })
        if data.is_valid():
            comprobante = crearComprobante(tipo_comprobante=data.validated_data.get('tipoComprobante'), pedido=data.validated_data.get(
                'pedidoId'), observaciones=data.validated_data.get('observaciones'))
            print(comprobante)
            if type(comprobante) == ComprobanteModel:
                data = ComprobanteModelSerializer(instance=comprobante)
                return Response(data={
                    "success": True,
                    "content": data.data,
                    "message": "comprobante creado exitosamente"
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(data={
                    "success": False,
                    "content": comprobante,
                    "message": "no se pudo crear el comprobante"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={
                "success": False,
                "content": data.errors,
                "message": "error al crear el comprobante"
            }, status=status.HTTP_400_BAD_REQUEST)
