from django.db import models
from datetime import date, datetime
from django.utils import timezone
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
    usuarioCorreo = models.EmailField(
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

    def __str__(self):
        return self.usuarioNombre + ' ' + self.usuarioApellido

    class Meta:
        # modifica el nombre de la tabla en la bd
        db_table = 'usuarios'
        # sirve para hacer unica una conjugacion de dos o mas columnas
        indexes = [models.Index(fields=['-usuarioCorreo', 'usuarioDni'])]
        unique_together = ['usuarioCorreo', 'usuarioDni']
        verbose_name = "usuario"
        verbose_name_plural = 'usuarios'
        ordering = ['-usuarioCorreo', 'usuarioNombre']


def anio_actual():
    return date.today().year


def opciones_anio():
    return [(anio, anio) for anio in range(1990, date.today().year+1)]


class LibroModel(models.Model):
    libroId = models.AutoField(
        primary_key=True,
        unique=True,
        null=False,
        db_column='id'
    )
    libroNombre = models.CharField(
        max_length=45,
        null=False,
        db_column='nombre',
        verbose_name='Nombre del Libro',
        help_text='Ingrese un nombre valido'
    )
    libroEdicion = models.IntegerField(
        db_column='edicion',
        null=False,
        choices=opciones_anio(),
        verbose_name='Año de edicion',
        help_text='Ingrese el año de la edicion',
        default=anio_actual,
    )
    libroAutor = models.TextField(
        db_column='autor',
        null=False,
        verbose_name='Autor del libro',
        help_text='Ingrese el autor'
    )
    libroCantidad = models.IntegerField(
        db_column='cantidad',
        verbose_name='Cantidad',
        default=0
    )

    createdAt = models.DateTimeField(
        auto_now_add=True, db_column='created_at', null=False)
    updatedAt = models.DateTimeField(auto_now=True, db_column='updated_at')
    deletedAt = models.DateTimeField(db_column='deleted_at', null=True)

    def __str__(self):
        return self.libroNombre

    class Meta:
        db_table = 'libros'

        unique_together = [['libroNombre', 'libroEdicion', 'libroAutor']]
        verbose_name = 'libro'
        verbose_name_plural = 'libros'
        ordering = ['-libroEdicion', '-libroCantidad', 'libroNombre']


class PrestamoModel(models.Model):
    prestamoId = models.AutoField(
        primary_key=True,
        unique=True,
        db_column='id'
    )
    prestamoFechaInicio = models.DateField(
        default=timezone.now,
        db_column='fecha_inicio',
        verbose_name='Fecha de inicio del prestamo'
    )
    prestamoFechaFin = models.DateField(
        db_column='fecha_fin',
        verbose_name='Fecha de fin del prestamo',
        null=False
    )
    prestamoEstado = models.BooleanField(
        db_column='estado',
        default=True,
        verbose_name='Estado del prestamo',
        help_text='Indique el estado del prestamo'
    )
    # opciones para la eliminacion de una PK con relacion
    # CASCADE -> elimina primero la pk y luego las fk
    # PROTECT -> no permite la eliminacion de la pk, si tiene relaciones
    # SET_NULL -> elimina la pk y posteriormente todas sus fk cambian d valor a null
    # DO_NOTHING -> elimina la pk y aun mantiene el valor de sus fk (mala integridad)
    # RESTRICT -> no permite la eliminacion, pero lanzara un error de tipo RestrictedError

    usuario = models.ForeignKey(
        to=UsuarioModel,
        db_column='usuario_id',
        on_delete=models.CASCADE,
        related_name='usuarioPrestamos',
        verbose_name='Usuario',
        help_text='seleccione el usuario a prestar'
    )
    libro = models.ForeignKey(
        to=LibroModel,
        db_column='libro_id',
        on_delete=models.PROTECT,
        related_name='libroPrestamos',
        verbose_name='Libro',
        help_text='seleccione el libro a prestar'
    )

    class Meta:
        db_table = 'prestamos'
        verbose_name = 'prestamo'
        verbose_name_plural = 'prestamos'
        ordering = ['-prestamoFechaInicio']
