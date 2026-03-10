from  .utils import UsuarioService
from django.contrib import messages
from db_connection import MongoDBConnection
from datetime import datetime

mongo = MongoDBConnection()

def crear_admin():
    try:
        # Crear usuario
        UsuarioService().crear_usuario(
            'admin', 
            'admin@admin.admin', 
            'admin',
            'Administrador',
            'superuser'
        )
        print('Usuario admin registrado exitosamente')
    except Exception as e:
        print(f'Error al registrar admin: {str(e)}')