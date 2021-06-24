from django.contrib.auth.models import BaseUserManager
# BaseUserManager => sirve para modificar el comportamiento de la creacion de un usuario por consola


class UsuarioManager(BaseUserManager):
    """Clase que sirve para modificar el comportamiento del modelo auth_user de django"""

    def create_user(self, email, nombre, apellido, tipo, telefono, password=None):
        """Creacion de un usuario comun"""
        if not email:
            raise ValueError(
                "el usuario debe tener obligatoriamente un correo")

        # normalizo el correo, que aparte de validar si hay un @ y un ., lo lleva todo a lowercase y quita espacios al inicio y al final
        email = self.normalize_email(email)
        # creo mi objeto de usuario pero aun no se guarda en la bd
        nuevoUsuario = self.model(
            usuarioCorreo=email, usuarioNNombre=nombre, usuarioApellido=apellido, usuarioTipo=tipo, usuarioTelefono=telefono)
        # ahora encripto la password
        nuevoUsuario.set_password(password)
        # guardo en la bd
        # self._db -> sirve para referenciar a la bd en el caso que nosotros tengamos varias conexiones en nuestro proyecto django
        nuevoUsuario.save(using=self._db)
        return nuevoUsuario

    def create_superuser(self, usuarioCorreo, usuarioNombre, usuarioApellido, usuarioTipo, usuarioTelefono, password):
        """Creacion de un nuevo super usuario para que pueda acceder al panel administrativo y algunas opciones adicionales"""
        usuario = self.create_user(
            usuarioCorreo, usuarioNombre, usuarioApellido, usuarioTipo, usuarioTelefono, password)
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save(using=self._db)
