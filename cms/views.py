from .models import PlatoModel
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
import os
import requests
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class Paginacion(PageNumberPagination):
    page_query_param = 'pagina'
    page_size = 3
    page_size_query_param = 'cantidad'
    max_page_size = 5

    def get_paginated_response(self, data):
        return Response(data={
            'paginacion': {
                'paginaContinua': self.get_next_link(),
                'paginaPrevia': self.get_previous_link(),
                'total': self.page.paginator.count
            },
            'data': {
                "success": True,
                "content": data,
                "message": None
            }
        })


class ArchivosController(CreateAPIView):
    serializer_class = ArchivoSerializer

    def post(self, request: Request):
        data = self.serializer_class(data=request.FILES)

        if data.is_valid():
            url = request.META.get('HTTP_HOST')
            archivo = data.save()

            return Response(data={
                "success": True,
                "content": url+archivo,
                "message": "Archivo subido exitosamente"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                "success": False,
                "content": data.errors,
                "message": "Error al subir el archivo"
            }, status=status.HTTP_400_BAD_REQUEST)


class EliminarArchivoController(DestroyAPIView):
    serializer_class = EliminarArchivoSerializer

    def delete(self, request: Request):
        data = self.serializer_class(data=request.data)
        data.is_valid()
        print(data)
        archivo = settings.MEDIA_ROOT / data.validated_data.get("nombre")
        try:
            os.remove(archivo)
            return Response(data={
                "success": True,
                "content": None,
                "message": "Imagen eliminada exitosamente"
            })
        except:
            return Response(data={
                "success": False,
                "content": None,
                "message": "la imagen ya fue eliminada previamente"
            }, status=status.HTTP_200_OK)


class PlatosController(ListCreateAPIView):
    queryset = PlatoModel.objects.all()
    serializer_class = PlatoSerializer

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                "success": True,
                "content": data.data,
                "message": "Creacion de plato exitosa"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'success': False,
                'content': data.errors,
                "message": "Error al crear el plato"
            }, status=status.HTTP_400_BAD_REQUEST)


class CustomPayloadController(TokenObtainPairView):
    """Sirve para modificar el payload de la token de acceso"""
    permission_classes = [AllowAny]
    serializer_class = CustomPayloadSerializer

    def post(self, request):
        data = self.serializer_class(data=request.data)
        print(data.initial_data)
        if data.is_valid():
            return Response(data={
                "success": True,
                "content": data.validated_data,
                "message": "login exitoso"
            })
        else:
            return Response(data={
                "success": False,
                "content": data.errors,
                "message": "error de login"
            })


class RegistroUsuarioController(CreateAPIView):
    serializer_class = RegistroUsuarioSerializer

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data={
                "message": "usuario creado exitosamente",
                "data": data.data,
                "success": True
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": "Error al crear el usuario",
                "content": data.errors,
                "success": False
            })


class MesaController(ListAPIView):
    queryset = MesaModel.objects.all()
    pagination_class = Paginacion
    serializer_class = MesasSerializer


class PedidoController(CreateAPIView):
    serializer_class = PedidoSerializer

    def post(self, request: Request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            documento_cliente = data.validated_data.get('documento_cliente')
            if documento_cliente:
                if len(documento_cliente) == 8:
                    url = "https://apiperu.dev/api/dni/{}".format(
                        documento_cliente)
                    print("es un dni")
                elif len(documento_cliente) == 11:
                    url = "https://apiperu.dev/api/ruc/{}".format(
                        documento_cliente)
                    print("es un ruc")
                headers = {
                    'Authorization': 'Bearer feadd026d7a0d5c8f4340c60de023ed6a25536b14ee2bb94cae418a66f0f5319',
                    'Content-Type': 'application/json'
                }
                respuesta = requests.get(url=url, headers=headers)
                print(respuesta.json())
                print(respuesta.status_code)
            print(data.validated_data)
            return Response(data="ok")
        else:
            return Response(data={
                "success": False,
                "content": data.errors,
                "message": 'Error al crear el pedido'
            })
