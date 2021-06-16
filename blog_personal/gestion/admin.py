from django.contrib import admin
from .models import LibroModel, UsuarioModel, PrestamoModel
# Register your models here.


class LibroAdmin(admin.ModelAdmin):
    # para modificar la lista del modelo
    list_display = ['libroNombre', 'libroAutor', 'libroCantidad']
    search_fields = ['libroNombre', 'libroEdicion']
    list_filter = ['libroAutor']
    readonly_fields = ['libroId']


admin.site.register(LibroModel, LibroAdmin)
admin.site.register(UsuarioModel)
admin.site.register(PrestamoModel)
