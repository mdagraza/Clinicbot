from django.shortcuts import render, redirect
from django.contrib import messages
from Clinicbot.utils import UsuarioService
import bcrypt
from .decorators import *

# Inicializar servicio
usuario_service = UsuarioService()

@solo_superusuarios
def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email')
        password = request.POST.get('password')
        nombre_completo = request.POST.get('nombre_completo').strip()

        # Validar datos
        if not username or not email or not password:
            messages.error(request, 'Todos los campos son obligatorios')
            return render(request, 'registro.html')

        try:
            # Crear usuario
            usuario_service.crear_usuario(
                username, 
                email, 
                password,
                False, #Por defecto no es superusuario
                nombre_completo
            )
            messages.success(request, 'Usuario registrado exitosamente')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
            return render(request, 'registro.html', {"error": str(e), "user": username, "email": email})

    return render(request, 'registro.html')

def login_view(request):
    if request.user and request.user.get('username'):
        messages.info(request, "Ya estas autenticado")
        return redirect('home')
        #return redirect(request.path)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if usuario_service.autenticar_usuario(username, password):
            #Verificar usuario activo
            if not usuario_service.usuario_activo(username):
                messages.error(request, 'Usuario inactivo. Contacta al administrador.')
                return render(request, 'home.html', {"error": 'Usuario inactivo. Contacta al administrador.'})
            # Guardar en sesión
            request.session['username'] = username
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect('home')
        else:
            messages.error(request, 'Credenciales inválidas')
            return render(request, 'home.html', {"error": 'Credenciales inválidas'})

    return render(request, 'login.html')

@login_required
def dashboard(request):
    # Listar usuarios (solo para ejemplo)
    usuarios = usuario_service.listar_usuarios()
    return render(request, 'dashboard.html', {'usuarios': usuarios})

def logout_view(request):
    # Limpiar sesión
    request.session.flush()
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('home')