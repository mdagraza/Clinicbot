from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db_connection import MongoDBConnection
from datetime import datetime
from api.tokens import TokenManager
from Clinicbot.utils import UsuarioService

from api.schemas.schemas import token_schema
from api.schemas.validator import validate_json

mongo = MongoDBConnection()

################## GESTION TOKENS ##################
class TokenView(APIView):
    """
    Endpoint de la API para autenticación y gestión de tokens.
    
    Este endpoint gestiona el inicio de sesión de usuarios y genera tokens de acceso requeridos
    para acceder a los endpoints protegidos de la API.
    """
    def __init__(self):
        self.users = mongo.get_collection_db_usuarios()
        self.tokens = mongo.get_collection_db_usuarios('api_tokens')
        self.token_manager = TokenManager()
    
    def post(self, request):
        """
        Autenticar usuario y generar token de acceso.
        
        Parámetros:<br/>
            user: Nombre de usuario para autenticación<br/>
            pass: Contraseña del usuario<br/>
            expires: Tiempo de expiración del token en horas (por defecto: 720)
            
        Devuelve:<br/>
            Token de acceso con información de expiración
        """
        username = request.data.get('user', '')
        password = request.data.get('pass', '')
        expires = request.data.get('expires', 720) #Debe pasarse en horas
        
        # Verificar credenciales
        user = self.users.find_one({"username": username})
        
        if not user or not self.verify_password(username, password):
            return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generar token
        token = self.token_manager.generate_token(str(user['_id']), expires)
        
        return Response({
            "access_token": token,
            "token_type": "Bearer Token",
            "expires_in_hours": expires,
            "date_expires": datetime.fromisoformat(str(self.tokens.find_one({"token": token})["expires_at"])).strftime("%d/%m/%Y %H:%M"),
            "date_expires_iso": str(self.tokens.find_one({"token": token})["expires_at"])
        })
    
    def verify_password(self, u_username, u_password):
        return UsuarioService().autenticar_usuario(u_username, u_password)