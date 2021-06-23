from django.urls import path
from .views import LibroController, LibrosController, PrestamoController, PrestamosController, UsuarioController, UsuariosController, busqueda_edicion, busqueda_libros

urlpatterns = [
    path('libros', LibrosController.as_view(), name='create-read-libros'),
    path('libros/<int:id>', LibroController.as_view()),
    path('busqueda_libros', busqueda_libros),
    path('busqueda_edicion', busqueda_edicion),
    path('usuarios', UsuariosController.as_view()),
    path('prestamos', PrestamosController.as_view()),
    path('prestamos/<int:id>', PrestamoController.as_view()),
    path('usuarios/<int:id>', UsuarioController.as_view()),
]
