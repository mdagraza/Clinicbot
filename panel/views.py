from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import UsuarioService
import bcrypt
from .decorators import *

# Inicializar servicio
usuario_service = UsuarioService()

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
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
                password
            )
            messages.success(request, 'Usuario registrado exitosamente')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
            return render(request, 'registro.html', {"error": str(e), "user": username, "email": email})

    return render(request, 'registro.html')

def login_view(request):
    if request.user and request.user.get('username'):
        messages.info(request, "Ya estas autenticado")
        return redirect('home2')
        #return redirect(request.path)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if usuario_service.autenticar_usuario(username, password):
            # Guardar en sesión
            request.session['username'] = username
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect('home2')
        else:
            messages.error(request, 'Credenciales inválidas')
            return render(request, 'login.html', {"error": 'Credenciales inválidas'})

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
    return redirect('home2')

@login_required
def cambiar_contrasena(request):
    if not request.user:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    if request.method == 'POST':
        clave_actual = request.POST.get('clave_actual')
        nueva_clave = request.POST.get('nueva_clave')
        confirmar_clave = request.POST.get('confirmar_clave')
        
        # Validar que las claves coincidan
        if nueva_clave != confirmar_clave:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'cambiar_contrasena.html')
        
        # Obtener usuario actual
        usuario = usuario_service.obtener_usuario(request.user['username'])
        
        # Verificar contraseña actual
        if not bcrypt.checkpw(clave_actual.encode('utf-8'), usuario['password']):
            messages.error(request, 'Contraseña actual incorrecta')
            return render(request, 'cambiar_contrasena.html')
        
        # Hashear nueva contraseña
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(nueva_clave.encode('utf-8'), salt)
        
        # Actualizar contraseña
        usuario_service.collection.update_one(
            {'username': request.user['username']},
            {'$set': {'password': hashed_password}}
        )
        
        messages.success(request, 'Contraseña cambiada exitosamente')
        return redirect('dashboard')
    
    return render(request, 'cambiar_contrasena.html')