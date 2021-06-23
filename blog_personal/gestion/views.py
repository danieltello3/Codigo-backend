from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import api_view
from .models import LibroModel, PrestamoModel, UsuarioModel
from .serializers import (BusquedaLibroSerializer,
                          LibroSerializer, PrestamoNestedSerializer,
                          PrestamoSerializer, PrestamoUsuarioSerializer, UsuarioNestedSerializer,
                          UsuarioSerializer)
from rest_framework.pagination import PageNumberPagination
# crear y listar todos los libros


class PaginacionPersonalizada(PageNumberPagination):
    # es el nombre de la variable que usaremos en la paginacion, su valor x default es page
    page_query_param = 'pagina'
    # es el valor predeterminado para la cantidad de items por pagina
    page_size = 2
    # es el nombre de la variable que usaremos para la cantidad de elementos que el usuario desea
    page_size_query_param = 'cantidad'
    # si el usuario me manda un elemento mayor que el max_page_size entonces usaremos el max_page_size (el tope de elementos por hoja)
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(data={
            'paginacion': {
                'paginaContinua': self.get_next_link(),
                'paginaPrevia': self.get_previous_link(),
                'total': self.page.paginator.count
            },
            'data': data
        }
        )


class LibrosController(ListCreateAPIView):
    # todas las clases genericas necesitan un query_set y un serializer_class
    # queryset = la consulta que hara a la bd cuando se llame a esta clase en un determinado metodo
    queryset = LibroModel.objects.all()  # SELECT * FROM libros
    # serializer_class = encargado de transformar la data que llega y que se envia al cliente
    serializer_class = LibroSerializer
    pagination_class = PaginacionPersonalizada

    # def get(self, request):
    #     # en el request se almacenan todos los datos que me manda el front(headers,body,cookies,auth)

    #     print(self.get_queryset())
    #     libros = self.get_queryset()
    #     respuesta = self.serializer_class(instance=libros, many=True)
    #     print(respuesta.data)
    #     return Response(data={
    #         'success': True,
    #         'content': respuesta.data,
    #         'message': None
    #     }, status=200)

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


class LibroController(RetrieveUpdateDestroyAPIView):
    queryset = LibroModel.objects.all()
    serializer_class = LibroSerializer

    def get(self, request: Request, id):
        libro = LibroModel.objects.filter(libroId=id).first()
        if libro is not None:
            libroSerializado = self.serializer_class(instance=libro)
            return Response(data={
                'success': True,
                'content': libroSerializado.data,
                'message': None
            }, status=status.HTTP_200_OK)
        else:
            return Response(data={
                "message": "Libro no encontrado",
                "content": None,
                "success": False
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request: Request, id):
        libro = LibroModel.objects.filter(libroId=id).first()
        if libro:
            data = self.serializer_class(data=request.data)
            libro_actualizado = self.serializer_class().update(
                instance=libro, validated_data=data.initial_data)
            print(libro_actualizado)
            return Response(data='ok')

        else:
            return Response(data={
                'success': False,
                'message': "No se encontro el libro",
                'content': None
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, id):
        libro = LibroModel.objects.filter(libroId=id).first()
        libro.deletedAt = now()
        libro.save()
        # libro.delete() => para eliminar el registro de la base de datos y retornara el total de registros eliminados
        data = self.serializer_class(instance=libro)
        return Response(data={
            'success': True,
            'content': data.data,
            'message': "se inhabilito el libro exitosamente"
        })


@api_view(http_method_names=['GET'])
def busqueda_libros(request: Request):
    print(request.query_params)
    nombre = request.query_params.get('nombre')
    autor = request.query_params.get('autor')

    # resultado = LibroModel.objects.filter(libroNombre__contains=nombre if nombre else '', libroAutor__contains=autor if autor else '').order_by('libroNombre').all()
    if nombre and autor:
        resultado = LibroModel.objects.filter(
            libroNombre__contains=nombre, libroAutor__contains=autor).order_by('libroNombre').all()
    elif nombre:
        resultado = LibroModel.objects.filter(
            libroNombre__contains=nombre).order_by('libroNombre').all()
    elif autor:
        resultado = LibroModel.objects.filter(
            libroAutor__contains=autor).order_by('libroNombre').all()
    else:
        resultado = LibroModel.objects.all()

    resultadoSerializado = LibroSerializer(instance=resultado, many=True)

    return Response(data={
        'success': True,
        'content': resultadoSerializado.data,
        'message': None
    })


@api_view(http_method_names=['GET'])
def busqueda_edicion(request: Request):
    # inicio = int(request.query_params.get('inicio'))
    # fin = int(request.query_params.get('fin'))
    param_serializados = BusquedaLibroSerializer(data=request.query_params)
    if param_serializados.is_valid():
        print(param_serializados.validated_data)
        resultado = LibroModel.objects.filter(libroEdicion__range=(param_serializados.validated_data.get(
            'inicio'), param_serializados.validated_data.get('fin'))).order_by('libroEdicion').all()

        resultadoSerializado = LibroSerializer(instance=resultado, many=True)

        return Response(data={
            'success': True,
            'content': resultadoSerializado.data,
            'message': None
        })
    else:
        return Response(data={
            'success': False,
            'content': param_serializados.errors,  # resultadoSerializado.data,
            'message': None
        })


class UsuariosController(ListCreateAPIView):
    queryset = UsuarioModel.objects.all()
    serializer_class = UsuarioSerializer
    pagination_class = PaginacionPersonalizada


class PrestamosController(CreateAPIView):
    queryset = PrestamoModel.objects.all()
    serializer_class = PrestamoSerializer

    def post(self, request: Request):
        data = request.data
        nuevoPrestamo = PrestamoSerializer(data=data)
        if nuevoPrestamo.is_valid():
            respuesta = nuevoPrestamo.save()
            if type(respuesta) is PrestamoModel:
                # libro: LibroModel = LibroModel.objects.filter(
                #     libroId=data.get('libro')).first()
                # libro.libroCantidad = libro.libroCantidad - 1
                # libro.save()
                return Response(data={
                    'success': True,
                    'content': nuevoPrestamo.data,
                    'message': "Prestamos agregado exitosamente"
                }, status=status.HTTP_201_CREATED)

        return Response(data={
            'success': False,
            'content': nuevoPrestamo.errors,
            'message': "Error al crear el prestamo"
        }, status=status.HTTP_400_BAD_REQUEST)


class PrestamoController(RetrieveAPIView):
    queryset = PrestamoModel.objects.all()
    serializer_class = PrestamoUsuarioSerializer

    def get(self, request, id):
        prestamo = PrestamoModel.objects.filter(prestamoId=id).first()
        if prestamo:
            data = self.serializer_class(instance=prestamo)
            return Response(data={
                "success": True,
                "content": data.data,
                "message": None
            })
        else:
            return Response(data={
                "success": False,
                "content": None,
                "message": "Prestamo no existe",
            }, status=status.HTTP_404_NOT_FOUND)


class UsuarioController(RetrieveAPIView):
    queryset = UsuarioModel.objects.all()
    serializer_class = UsuarioNestedSerializer

    def get(self, request, id):
        usuario = UsuarioModel.objects.filter(usuarioId=id).first()
        if usuario:
            data = self.serializer_class(instance=usuario)
            return Response(data={
                "success": True,
                "content": data.data,
                "message": None
            })
        else:
            return Response(data={
                "success": False,
                "content": None,
                "message": "usuario no existe",
            }, status=status.HTTP_404_NOT_FOUND)
