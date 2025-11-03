from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from .tokens import TokenManager

from db_connection import MongoDBConnection
mongo = MongoDBConnection()

def token_required(view_func): #PENDIENTE REVISAR : Se deberian devolver los datos segun el tipo de usuario, si es admin todos los datos, si es usuario normal solo los suyos
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        # Obtener el token del encabezado
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        #Se filtra cuando la peticion es interna de la web
        if auth_header.startswith('Interno '):
            user_id = auth_header.split(' ')[1]
            if not mongo.get_collection_db_usuarios().find_one({"_id": ObjectId(user_id)}): #Solo se verifica que el usuario exista
                return Response({"error": "Se requiere Bearer token"}, status=status.HTTP_401_UNAUTHORIZED)

            request.user_id = user_id
            return view_func(self, request, *args, **kwargs)
        
        if not auth_header.startswith('Bearer '):
            return Response({"error": "Se requiere Bearer token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = auth_header.split(' ')[1]
        
        # Validar token
        token_manager = TokenManager()
        token_data = token_manager.validate_token(token)
        
        if not token_data:
            return Response({"error": "Token inválido o expirado"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Añadir información del usuario a la solicitud
        request.user_id = token_data['user_id']
        
        return view_func(self, request, *args, **kwargs)
    
    return wrapper