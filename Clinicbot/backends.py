from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject

from .utils import UsuarioService

UserModel = get_user_model()

class MongoBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        usuario_service = UsuarioService()

        if usuario_service.validar_credenciales(username, password):
            # Retornar un User-like object para Django
            return MongoUser(username)
        return None

    def get_user(self, user_id):
        # Django lo usa para recuperar usuarios desde sesiones
        usuario_service = UsuarioService()
        usuario = usuario_service.obtener_usuario_por_id(user_id)
        if usuario:
            return MongoUser(usuario['username'])
        return None

class MongoUser:
    """
    Representación básica de un usuario compatible con Django
    """
    def __init__(self, username):
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_staff = False  # Cambia según tus permisos
        self.is_superuser = False

    def get_username(self):
        return self.username

    def __str__(self):
        return self.username

    def save(self):
        pass

    def delete(self):
        pass

    @property
    def pk(self):
        return self.username