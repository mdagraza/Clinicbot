from Clinicbot.utils import UsuarioService
from django.contrib import messages
from db_connection import *
from datetime import datetime

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


def datos_prueba():
    # Conectar con MongoDB
    collection = get_db_pacientes()
    collection2 = get_db_muestras()

    if list(collection.find()): # Comprobar si ya hay pacientes en la colección convertiendo a lista
        return  # Si ya hay pacientes, no se añaden más

    pacientes = [{
            "nombre": "Nombre_1",
            "apellidos": "Apellidos_1",
            "ident_paciente": "1234567",
            "edad": 30,
            "email": "nombre_1@test.com",
            "genero": "Otro",
            "gr_sanguineo": "A+"
            },
            {
            "nombre": "Nombre_2",
            "apellidos": "Apellidos_2",
            "ident_paciente": "2345678",
            "edad": 25,
            "email": "nombre_2@test.com",
            "genero": "Mujer",  
            "gr_sanguineo": "B-"
            },
            {
            "nombre": "Nombre_3",
            "apellidos": "Apellidos_3",
            "ident_paciente": "3456789",
            "edad": 40,
            "email": "nombre_3@test.com",
            "genero": "Hombre",
            "gr_sanguineo": "0+"
            }]
    collection.insert_many(pacientes)

    muestras = [{
                #"paciente_id": collection.find_one({"ident_paciente": "1234567"})["_id"],
                "identificador": "YY.1234567",
                "color": "Rojo",
                "posicion": 123123,
                "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
            },
            {
                #"paciente_id": collection.find_one({"ident_paciente": "2345678"})["_id"],
                "identificador": "YY.2345678",
                "color": "Azul",
                "posicion": 234234,
                "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
            },
            {
                #"paciente_id": collection.find_one({"ident_paciente": "3456789"})["_id"],
                "identificador": "YY.3456789",
                "color": "Verde",
                "posicion": 345345,
                "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
            }]
    collection2.insert_many(muestras)

    print('Datos de prueba añadidos exitosamente')