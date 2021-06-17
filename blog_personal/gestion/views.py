from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import LibroModel
from .serializers import LibroSerializer

# crear y listar todos los libros


class LibrosController(ListCreateAPIView):
    # todas las clases genericas necesitan un query_set y un serializer_class
    # queryset = la consulta que hara a la bd cuando se llame a esta clase en un determinado metodo
    queryset = LibroModel.objects.all()  # SELECT * FROM libros
    # serializer_class = encargado de transformar la data que llega y que se envia al cliente
    serializer_class = LibroSerializer

    def get(self, request):
        # en el request se almacenan todos los datos que me manda el front(headers,body,cookies,auth)

        print(self.get_queryset())
        libros = self.get_queryset()
        respuesta = self.serializer_class(instance=libros, many=True)
        print(respuesta.data)
        return Response(data={
            'success': True,
            'content': respuesta.data,
            'message': None
        }, status=200)

    def post(self, request: Request):
        # la informacion mandada por el front (body) se recibira por el atributo data
        print(request.data)
        data = self.serializer_class(data=request.data)
        # el metodo is_valid() validara si la data pasada es o no es correcta, si cumple con lo necesitado para crear un nuevo libro, retornara un bool
        # adicionalmente podemos indicar un parametro llamado raise_exception => True, lanzara los errores que no permite que la data sea valida
        valida = data.is_valid()
        if valida:
            # el metodo save() corresponde al serializador que cuando es de tipo ModelSerializer implementa los metodos de guardado y actualizacion en la bd
            data.save()
            # el atributo data me dara un diccionario ordenado con la informacion guardada en la bd(incluyendo campos de solo lectura) id
            return Response(data={
                'success': True,
                "content": data.data,
                'message': "libro creado exitosamente"
            }, status=status.HTTP_201_CREATED)
        else:
            # el atributo erros me indicara todos los erros que no han permitido que la informacion sea valida
            return Response(data={
                'success': False,
                'content': data.errors,
                'message': 'la data no es valida'
            }, status=status.HTTP_400_BAD_REQUEST)
