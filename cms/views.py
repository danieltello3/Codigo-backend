from .models import PlatoModel
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
import os
from django.conf import settings
# Create your views here.


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
        print(request.FILES)
        return Response(data='ok')


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
