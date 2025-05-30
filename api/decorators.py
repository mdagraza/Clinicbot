from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .tokens import TokenManager

def token_required(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        # Obtener el token del encabezado
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
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