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
                      es_superuser=False): 
        
        ##Formatear datos
        email = email.lower()
        
        #Verificar que el usuario no sea nada relativo a admin
        if not es_superuser and ('admin' in username.lower()):
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
            'numUser' : self.obtener_numUser(),
            'username': username,
            'email': email,
            'password': hashed_password,
            'es_superuser': es_superuser, 
            'es_staff': es_superuser,   
            'activo': True, 
            'permisos': ['usuario_normal'] if not es_superuser else ['superuser']
        }

        return self.collection.insert_one(usuario)

    def validar_credenciales(self, username, password):
        # Buscar usuario
        usuario = self.collection.find_one({'username': username})
        
        if usuario:
            # Verificar contraseña
            return bcrypt.checkpw(password.encode('utf-8'), usuario['password'])
        return False

    def obtener_usuario(self, username):
        return self.collection.find_one({'username': username})
    
    def obtener_usuario_por_id(self, user_id):
        print(f"Obteniendo usuario con ID: {user_id}")
        return self.collection.find_one({'numUser': user_id})

    def listar_usuarios(self):
        return list(self.collection.find({}, {'password': 0}))  # Excluir contraseñas
    
    def es_superuser(self, username):
        usuario = self.obtener_usuario(username)
        return usuario and usuario.get('es_superuser', False)
    
    def obtener_permisos(self, username):
        usuario = self.obtener_usuario(username)
        return usuario.get('permisos', []) if usuario else []
    
    def obtener_numUser(self):
        # Buscar el documento con el numUser más alto
        max_user = self.collection.find_one(sort=[("numUser", -1)])
    
        if max_user and "numUser" in max_user:
            return max_user["numUser"] + 1
        else:
            return 1
    

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
                'permisos': self.usuario_service.obtener_permisos(username)
            }
        else:
            request.user = None
        
        return self.get_response(request)