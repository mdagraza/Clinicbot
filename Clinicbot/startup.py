from Clinicbot.utils import UsuarioService
from django.contrib import messages

def crear_admin():
    try:
        # Crear usuario
        UsuarioService().crear_usuario(
            'admin', 
            'admin@admin.admin', 
            'admin',
            True
        )
        print('Usuario admin registrado exitosamente')
    except Exception as e:
        print(f'Error al registrar admin: {str(e)}')