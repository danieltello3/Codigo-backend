from django.urls import path
from .views import (ArchivosController,
                    EliminarArchivoController, PlatosController, CustomPayloadController)

urlpatterns = [
    path('platos', PlatosController.as_view()),
    path('subirImagen', ArchivosController.as_view()),
    path('eliminarImagenes', EliminarArchivoController.as_view()),
    path('login-custom', CustomPayloadController.as_view())
]
