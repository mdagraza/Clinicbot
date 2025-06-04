from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject

from django.contrib.auth.models import AnonymousUser

from .utils import UsuarioService

UserModel = get_user_model()
# Instancia global del servicio
usuario_service = UsuarioService()

class MongoBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if usuario_service.validar_credenciales(username, password):
            datos = usuario_service.obtener_usuario(username)
            if datos:
                return MongoUser(datos)
        return None

    def get_user(self, user_id):
        datos = usuario_service.obtener_usuario_por_id(user_id)
        if datos:
            return MongoUser(datos)
        return AnonymousUser()
    
class DummyField:
    # Este es el campo "pk" que Django espera,
    # solo para evitar el error 'str' object has no attribute 'value_to_string'
    def __init__(self, name):
        self.name = name

    def value_to_string(self, obj):
        # Devuelve el valor del campo en string
        return str(getattr(obj, self.name))

class DummyMeta:
    # Simula la meta información de Django, con un pk que es DummyField
    def __init__(self, pk_name):
        self.pk = DummyField(pk_name)

class MongoUser:
    def __init__(self, data):
        self.id = str(data['numUser'])
        self.username = data['username']
        #self.is_active = True
        #self.is_authenticated = True
        self.es_superuser = data.get('es_superuser', False)
        self.permisos = data.get('permisos', [])
        self._meta = DummyMeta('id')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_staff(self):
        return self.es_superuser

    @property
    def is_superuser(self):
        return self.es_superuser

    def get_username(self):
        return self.username
    
    def get_session_auth_hash(self):
        return ''  # Cambiar a un hash real
    
    def save(self, *args, **kwargs):
        # Aquí puedes implementar la actualización de last_login en MongoDB
        # Si no quieres implementarlo aún, pon un pass para evitar errores
        pass

    def __str__(self):
        return (
            f"<MongoUser "
            f"username={self.username} | "
            f"pk={self.id} | "
            f"es_superuser={self.es_superuser} | "
            f"activo={self.is_active} | "
            f"permisos={self.permisos}>"
        )