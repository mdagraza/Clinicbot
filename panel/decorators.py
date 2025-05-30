from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import status

def solo_usuarios_normales(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if not request.session.get('username'):
            messages.error(request, 'Debes iniciar sesión')
            return redirect('login')
        
        # Verificar que NO sea superusuario
        if request.user and 'superuser' in request.user.get('permisos', []):
            messages.error(request, 'No tienes permisos para acceder')
            return redirect('home2')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def solo_superusuarios(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if not request.session.get('username'):
            messages.error(request, 'Debes iniciar sesión')
            return redirect('login')
        
        # Verificar que sea superusuario
        if not (request.user and 'superuser' in request.user.get('permisos', [])):
            messages.error(request, 'Acceso restringido a superusuarios')
            return redirect('home2')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar si hay un usuario en sesión
        if not request.session.get('username'):
            messages.warning(request, 'Debes iniciar sesión para acceder')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def login_required_rest(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verifica si el usuario está autenticado
        if not request.session.get('username'):
            return Response(
                {"error": "Autenticación requerida"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        return view_func(request, *args, **kwargs)
    return wrapper