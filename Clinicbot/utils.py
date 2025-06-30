from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt

class UsuarioService:
    def __init__(self):
        # Conexión a MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['Clinicbot-Usuarios']
        self.collection = self.db['usuarios']

    def crear_usuario(self, username, email, password, 
                      nombre_completo='', tipo_usuario='usuario'): 
        
        ##Formatear datos
        email = email.lower()
        
        #Verificar que el usuario no sea nada relativo a admin
        if not tipo_usuario==2 and ('admin' in username.lower()):
            raise ValueError("Nombre de usuario no válido")

        # Verificar si el usuario ya existe
        '''if self.collection.find_one({"username": username}):
            raise ValueError("Nombre de usuario ya en uso")'''
        
        if self.collection.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}}) or self.collection.find_one({"email": email}):
            raise ValueError("Nombre de usuario o email ya en uso")
        
        '''
            $regex: Permite realizar una búsqueda usando expresiones regulares.
            f"^{username}$": El patrón ^{username}$ asegura que la búsqueda sea exactamente para el valor de username, sin caracteres extra antes o después.
            "$options": "i": Esta opción hace que la búsqueda sea case-insensitive (sin tener en cuenta si es mayúscula o minúscula).
        '''

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        usuario = {
            'username': username,
            'nombre_completo': nombre_completo, 
            'email': email,
            'password': hashed_password,
            'activo': True,  # Por defecto, el usuario está activo
            'es_superuser': True if tipo_usuario == 2 else False,  # Si es superusuario
            'permisos': [tipo_usuario]
        }

        return self.collection.insert_one(usuario)
    
    def editar_usuario(self, id_usuario, username, email, password, 
                      nombre_completo='', tipo_usuario='usuario'): 
        ##Formatear datos
        email = email.lower()
        
        ##REVISAR | APUNTE : Al editar un usuario, no se debería cambiar el nombre de usuario
        #Verificar que el usuario no sea nada relativo a admin
        if not tipo_usuario==2 and ('admin' in username.lower()):
            raise ValueError("Nombre de usuario no válido")

        # Verificar si el usuario ya existe        
        '''if self.collection.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}}) or self.collection.find_one({"email": email}):
            raise ValueError("Nombre de usuario o email ya en uso")'''

        # Actualizar los datos del usuario
        update_data = {
            'username': username,
            'nombre_completo': nombre_completo, 
            'email': email,
            'es_superuser': True if tipo_usuario == 2 else False,  # Si es superusuario
            'permisos': [tipo_usuario]
        }

        # Si se proporciona una contraseña, se codifica y se agrega al update_data
        if password: 
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            update_data.update({'password': hashed_password}) # Se agrega la contraseña solo si se proporciona
        
        result = self.collection.update_one(
            {'_id': ObjectId(id_usuario)},
            {'$set': update_data}
        )
        
        return result

    def autenticar_usuario(self, username, password):
        # Buscar usuario
        usuario = self.collection.find_one({'username': username})
    
        if usuario:
            # Verificar contraseña
            return bcrypt.checkpw(password.encode('utf-8'), usuario['password'])
        return False

    def obtener_usuario(self, username):
        return self.collection.find_one({'username': username})

    def listar_usuarios(self):
        return list(self.collection.find({}, {'password': 0}))  # Excluir contraseñas
    
    def es_superuser(self, username):
        usuario = self.obtener_usuario(username)
        return usuario and usuario.get('es_superuser', False)
    
    def obtener_permisos(self, username):
        usuario = self.obtener_usuario(username)
        return usuario.get('permisos', []) if usuario else []
    
    def obtener_idUsuario(self, username):
        usuario = self.obtener_usuario(username)
        return str(usuario['_id']) if usuario else None
    
    def usuario_activo(self, username):
        usuario = self.obtener_usuario(username)
        return usuario and usuario.get('activo', False)


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.usuario_service = UsuarioService()

    def __call__(self, request):
        # Simular sesión (en producción, usar sesiones de Django)
        username = request.session.get('username')
        if username:
            request.user = {
                'username': username,
                'es_superuser': self.usuario_service.es_superuser(username),
                'permisos': self.usuario_service.obtener_permisos(username),
                'idUsuario': self.usuario_service.obtener_idUsuario(username),
            }
        else:
            request.user = None
        
        return self.get_response(request)