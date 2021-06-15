from django.db import models
from django.db.models import indexes

# Create your models here.


class UsuarioModel(models.Model):
    usuarioId = models.AutoField(
        primary_key=True, null=False, unique=True, db_column='id')
    usuarioNombre = models.CharField(
        max_length=25,
        null=False,
        db_column='nombre',
        # a continuacion son parametros para el panel administrativo
        # mostrara para que sirve en el form del panel administrativo
        verbose_name='Nombre del Usuario',
        help_text='Aqui debes ingresar el nombre'
    )
    usuarioApellido = models.CharField(
        max_length=25,
        null=False,
        db_column='apellido',
        verbose_name='Apellido del Usuario',
        help_text='Aqui debes ingresar el apellido'
    )
    correoUsuario = models.EmailField(
        max_length=50,
        db_column='correo',
        verbose_name='Correo del Usuario',
        help_text='Debes ingresar un correo valido'
    )
    usuarioDni = models.CharField(
        max_length=8,
        db_column='dni',
        verbose_name='Dni del Usuario',
        help_text='Ingrese un dni valido'
    )

    class Meta():
        # modifica el nombre de la tabla en la bd
        db_table = 'usuarios'
        # sirve para hacer unica una conjugacion de dos o mas columnas
        indexes = [models.Index(fields=['-usuarioCorreo', 'usuarioDni'])]
        unique_together = ['usuarioCorreo', 'usuarioDni']
        verbose_name = "usuario"
        verbose_name_plurar = 'usuarios'
