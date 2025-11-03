import bcrypt
from bson import ObjectId
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render
from panel.decorators import *
from db_connection import MongoDBConnection
from api.tokens import TokenManager

mongo = MongoDBConnection()

# Create your views here.
@login_required
def panel_datos(request, error=None):
    if request.method == 'POST':
        nombre = request.POST.get('nombre').strip()
        email = request.POST.get('email').strip()

        mongo.get_collection_db_usuarios().update_one(
            {"_id": ObjectId(request.user.get('idUsuario'))},
            {"$set": {"nombre_completo": nombre, "email": email}}
        )

    #Obtener datos del usuario desde la sesión
    usuario = mongo.get_collection_db_usuarios().find_one({"_id": ObjectId(request.user.get('idUsuario'))})
    datos = {
        'username': usuario.get('username', ''),
        'nombre_completo': usuario.get('nombre_completo', ''),
        'email': usuario.get('email', '')
    }  
    return render(request, 'datos.html', {"datos": datos, "error": request.session.pop('contrasena_error', None)}) 

@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        clave_actual = request.POST.get('current_password')
        nueva_clave = request.POST.get('new_password')
        confirmar_clave = request.POST.get('confirm_password')

        # Obtener usuario actual
        usuario = mongo.get_collection_db_usuarios().find_one({"_id": ObjectId(request.user.get('idUsuario'))})

        # Verificar contraseña actual
        if not bcrypt.checkpw(clave_actual.encode('utf-8'), usuario['password']):
            messages.error(request, 'Contraseña actual incorrecta')
            request.session['contrasena_error'] = 'Contraseña actual incorrecta.' #Se guarda el error en la sesión para mostrar en el panel de datos
            return redirect('panel_datos')
        
        # Validar que las claves no sean iguales
        if clave_actual == nueva_clave:
            messages.error(request, 'La contraseña nueva no puede ser igual a la actual')
            request.session['contrasena_error'] = 'La contraseña nueva no puede ser igual a la actual.' #Se guarda el error en la sesión para mostrar en el panel de datos
            return redirect('panel_datos')
        
        # Validar que las claves coincidan
        if nueva_clave != confirmar_clave:
            messages.error(request, 'La nueva contraseña y la confirmación no coinciden')
            request.session['contrasena_error'] = 'La nueva contraseña y la confirmación no coinciden.' #Se guarda el error en la sesión para mostrar en el panel de datos
            return redirect('panel_datos')
        
        # Hashear nueva contraseña
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(nueva_clave.encode('utf-8'), salt)
        
        # Actualizar contraseña
        mongo.get_collection_db_usuarios().update_one(
            {"_id": ObjectId(request.user.get('idUsuario'))},
            {'$set': {'password': hashed_password}}
        )
        messages.success(request, 'Contraseña cambiada exitosamente')
        request.session['contrasena_error'] = 'Contraseña cambiada exitosamente.'

    return redirect('panel_datos')

@login_required
def panel_tokens(request):
    if request.method == 'POST':
        expires = int(request.POST.get('duration', '30')) * 24  # Por defecto 30 días
        
        token_manager = TokenManager()
        token_manager.generate_token(request.user.get('idUsuario'), expires)
     
    # Obtener tokens desde la base de datos que sigan activos
    tokens = mongo.get_collection_db_usuarios("api_tokens").find({"user_id": ObjectId(request.user.get('idUsuario')), "expires_at": {"$gt": datetime.now()}})

    tokens = [
        {
            "id": str(token["_id"]),
            "token": token.get("token", ""),
            "fecha_creacion": token.get("created_at", ""),
            "fecha_expiracion": token.get("expires_at", ""),
        }
        for token in tokens
    ]
   
    return render(request, 'tokens.html', {"tokens": tokens})

@login_required
def panel_usuarios(request):
    # Obtener usuarios desde la base de datos
    usuarios = list(mongo.get_collection_db_usuarios().find({}, {'password': 0}))  # Excluir contraseñas
    # Formatear usuarios para la plantilla
    usuarios = [
    {
        "id": str(usuario["_id"]),
        "username": usuario.get("username", ""),
        "nombre_completo": usuario.get("nombre_completo", ""),
        "email": usuario.get("email", ""),
        "es_superuser": usuario.get("es_superuser", ""),
        "activo": usuario.get("activo", ""),
        "permisos": usuario.get("permisos", [])
    }
    for usuario in usuarios
    ]

    return render(request, 'usuarios.html', {"usuarios": usuarios})



'''
usuarios = db_pacientes.find().sort("apellidos",1)
    usuarios = [
    {
        "id": str(usuario["_id"]),
        "nombre": usuario.get("nombre", ""), #Si no encuentra la key, se asigna un valor por defecto a la variable
        "apellidos": usuario.get("apellidos", ""),
        "edad": usuario.get("edad", ""),
        "email": usuario.get("email", ""),
        "genero": usuario.get("genero", ""),
        "gr_sanguineo": usuario.get("gr_sanguineo", "")
    }
    for usuario in usuarios
    ]


'''