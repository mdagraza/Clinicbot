from bson import ObjectId
from django.shortcuts import render
from panel.decorators import *
from db_connection import get_db_users

db_users = get_db_users()
# Create your views here.
@login_required
def panel_datos(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre').strip()
        email = request.POST.get('email').strip()

        db_users.update_one(
            {"_id": ObjectId(request.user.get('idUsuario'))},
            {"$set": {"nombre_completo": nombre, "email": email}}
        )

    #Obtener datos del usuario desde la sesión
    usuario = db_users.find_one({"_id": ObjectId(request.user.get('idUsuario'))})

    print(request.user.get('idUsuario'))
    print(usuario)

    datos = {
        'username': usuario.get('username', ''),
        'nombre_completo': usuario.get('nombre_completo', ''),
        'email': usuario.get('email', '')
    }  
    return render(request, 'datos.html', {"datos": datos}) 

@login_required
def cambiar_contrasena(request):
    pass

@login_required
def panel_tokens(request):
    return render(request, 'tokens.html')

@login_required
def panel_usuarios(request):
    return render(request, 'usuarios.html')



'''
db_pacientes.update_one(
                {"_id": ObjectId(usuario_id)},
                {"$set": {"nombre": nombre, "apellidos": apellidos, "ident_muestra": ident_muestra, "ident_petri": ident_petri, "edad": int(edad), "email": email, "genero": genero, "gr_sanguineo": gr_sanguineo}}
            )

'''

'''
petri = db_petri.find({"identificador": patron_id_paciente})

'''


'''
@login_required
def cambiar_contrasena(request):
    
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

'''