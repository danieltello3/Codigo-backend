from .models import PlatoModel
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import *
# Create your views here.


class ArchivosController(CreateAPIView):
    serializer_class = ArchivoSerializer

    def post(self, request: Request):
        data = self.serializer_class(data=request.FILES)
        data.is_valid(raise_exception=True)
        data.save()
        return Response('ok')


class PlatosController(ListCreateAPIView):
    queryset = PlatoModel.objects.all()
    serializer_class = PlatoSerializer

    def post(self, request: Request):
        print(request.FILES)
        return Response(data='ok')
