from django.db import models
from authManager import UsuarioManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class PlatoModel(models.Model):
    platoId = models.AutoField(
        primary_key=True,
        null=False,
        db_column='id',
        unique=True
    )
    platoNombre = models.CharField(
        max_length=45,
        null=False,
        db_column='nombre',
        unique=True
    )
    platoPrecio = models.DecimalField(
        db_column='precio',
        null=False,
        decimal_places=2,
        max_digits=5
    )
    # ImageField => sirve para almacenar imagenes en el servidor, en la bd guardara la ubicacion del archivo y el archivo lo almacenara en el propio servidor

    platoFoto = models.ImageField(
        upload_to="platos",  # indicara la carpeta en la cual se debe de guardar dicho archivo
        db_column='foto',
        null=True,
    )
    platoCantidad = models.IntegerField(
        db_column='cantidad',
        default=0,
    )

    class Meta:
        db_table = 'platos'
        ordering = ['platoNombre']


class UsuarioModel(AbstractBaseUser, PermissionsMixin):
    """Modificar el modelo auth_user de la base de datos"""
    # si nosotros queremos modificar solamente los campos necesarios del modelo auth_user deberemos usar el AbstractUser(first_name, last_name, password)
    # si yo quiero resetear por completo mi auth_user, debemos usar el AbstractBaseUser
    # PermissionsMixin => es la clase encargada de dar todos los permisos a nivel administrativo

    TIPO_PERSONAL = [
        (1, 'ADMINISTRADOR'),
        (2, 'CAJERO'),
        (3, 'MOZO')
    ]

    usuarioId = models.AutoField(
        primary_key=True,
        unique=True,
        db_column='id'
    )
    usuarioNombre = models.CharField(
        max_length=20,
        null=False,
        db_column='nombre'
    )
    usuarioApellido = models.CharField(
        max_length=20,
        null=False,
        db_column='apellido'
    )
    usuarioCorreo = models.EmailField(
        db_column='correo',
        null=False
    )
    usuarioTipo = models.IntegerField(
        choices=TIPO_PERSONAL,
        db_column='tipo'
    )
    usuarioTelefono = models.CharField(
        max_length=10,
        db_column='telefono'
    )
    password = models.TextField()

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # comportamiento del modelo al momento de realizar la creacion del superusuario por consola

    objects = UsuarioManager

    # ahora defino que columna sera la encargada de validar que el usuario sea unico
    USERNAME_FIELD = 'usuarioCorreo'
    # sirve para indicar que campos se van a solicitar cuando se cree al superuser por consola
    REQUIRED_FIELDS = ['usuarioNombre', 'usuarioApellido', 'usuarioTipo']

    class Meta:
        db_table = 'usuarios'


class MesaModel(models.Model):
    mesaId = models.AutoField(
        primary_key=True,
        unique=True,
        null=False,
        db_column='id'
    )
    mesaDescripcion = models.CharField(
        max_length=10,
        null=False,
        db_column='descripcion'
    )
    mesaCapacidad = models.IntegerField(
        db_column='capacidad',
        null=False
    )

    class Meta:
        db_table = 'mesas'


class PedidosModel(models.Model):
    pedidoId = models.AutoField(
        primary_key=True,
        unique=True,
        null=False,
        db_column='id'
    )
    pedidoFecha = models.DateTimeField(
        db_column='fecha',
        auto_now=True,
    )
    pedidoTotal = models.DecimalField(
        db_column='total',
        decimal_places=2,
        max_digits=6
    )
    pedidoNombreCliente = models.CharField(
        max_length=45,
        db_column='nombre_cliente'
    )
    pedidoDocumentoCliente = models.CharField(
        max_length=12,
        db_column='documento_cliente'
    )

    usuario = models.ForeignKey(
        to=UsuarioModel,
        db_column='usuario_id',
        on_delete=models.PROTECT,
        related_name='usuarioPedido'
    )
    mesa = models.ForeignKey(
        to=MesaModel,
        db_column='mesa_id',
        on_delete=models.PROTECT,
        related_name='mesaPedido'
    )

    class Meta:
        db_table = 'pedidos'
        ordering = ['-pedidoFecha']


class DetalleModel(models.Model):
    detalleId = models.AutoField(
        primary_key=True,
        db_column='id',
        unique=True,
        null=False
    )
    detalleCantidad = models.IntegerField(
        db_column='cantidad',
        null=False
    )
    detalleSubTotal = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        db_column='sub_total'
    )

    pedido = models.ForeignKey(
        to=PedidosModel,
        db_column='pedido_id',
        on_delete=models.PROTECT,
        related_name='pedidoDetalles'
    )

    plato = models.ForeignKey(
        to=PlatoModel,
        db_column='plato_id',
        on_delete=models.PROTECT,
        related_name='platoDetalles'
    )

    class Meta:
        db_table = 'detalles'
