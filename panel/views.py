from django.shortcuts import render, redirect
from django.contrib import messages
from Clinicbot.utils import UsuarioService
import bcrypt
from .decorators import *
from .logs import log_action

# Inicializar servicio
usuario_service = UsuarioService()

@solo_superusuarios
def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        nombre_completo = request.POST.get('nombre_completo').strip()
        email = request.POST.get('email').strip()
        tipo_usuario = request.POST.get('tipo_usuario')
        password = request.POST.get('password')
        

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
                nombre_completo,
                tipo_usuario
            )
            messages.success(request, 'Usuario registrado exitosamente')
            return redirect('panel_usuarios')
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
            return render(request, 'registro.html', {"error": str(e), "user": username, "email": email}) ## ARREGLAR REVISAR

    return render(request, 'registro.html')

@login_required
def editar_usuario(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        username = request.POST.get('username').strip()
        nombre_completo = request.POST.get('nombre_completo').strip()
        email = request.POST.get('email').strip()
        tipo_usuario = request.POST.get('tipo_usuario')
        password = request.POST.get('password')

        try:
            # Editar usuario
            usuario_service.editar_usuario(
                usuario_id,
                username, 
                email, 
                password,
                nombre_completo,
                tipo_usuario
            )
            messages.success(request, 'Usuario editado exitosamente')
            return redirect('panel_usuarios')
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
            return render(request, 'registro.html', {"error": str(e), "user": username, "email": email}) ## ARREGLAR REVISAR

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
            log_action(request, 'LOGIN', 'SUCCESS', f'Usuario {username} inició sesión exitosamente.')
            return redirect('home')
        else:
            messages.error(request, 'Credenciales inválidas')
            log_action(request, 'LOGIN', 'FAILURE', f'Intento de inicio de sesión fallido para el usuario {username}.')
            return render(request, 'home.html', {"error": 'Credenciales inválidas'}) #REVISAR CAMBIAR a un redirect y pasarle el error como se hace en panel-admin en cambiar contraseña

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