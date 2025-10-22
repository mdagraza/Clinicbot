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
            'Administrador',
            'superuser'
        )
        print('Usuario admin registrado exitosamente')
    except Exception as e:
        print(f'Error al registrar admin: {str(e)}')


def datos_prueba():
    # Conectar con MongoDB
    db_pacientes = get_db_pacientes()
    db_muestras = get_db_muestras()
    db_petri = get_db_petri()

    if list(db_pacientes.find()): # Comprobar si ya hay pacientes en la colección convertiendo a lista
        return  # Si ya hay pacientes, no se añaden más

    pacientes = [{
            "nombre": "Miguel",
            "apellidos": "Dagraza Alonso",
            "ident_muestra": "1234567",
            "ident_petri": "1234",
            "edad": 30,
            "email": "nombre_1@test.com",
            "genero": "Otro",
            "gr_sanguineo": "A+"
            },
            {
            "nombre": "Antonio Manuel",
            "apellidos": "Zacarias Del Río Parísimo de la Vega Fernandez",
            "ident_muestra": "2345678",
            "ident_petri": "1235",
            "edad": 25,
            "email": "nombre_2@test.com",
            "genero": "Mujer",  
            "gr_sanguineo": "B-"
            },
            {
            "nombre": "Jesús",
            "apellidos": "Nazareno de la Cruz",
            "ident_muestra": "3456789",
            "ident_petri": "1236",
            "edad": 40,
            "email": "nombre_3@test.com",
            "genero": "Hombre",
            "gr_sanguineo": "0+"
            },
            {
            "nombre": "Jesús",
            "apellidos": "Nazareno de la Cruz",
            "ident_muestra": "356984",
            "ident_petri": "2654",
            "edad": 40,
            "email": "nombre_3@test.com",
            "genero": "Hombre",
            "gr_sanguineo": "0+"
            }]
    db_pacientes.insert_many(pacientes)

    muestras = [{
                #"paciente_id": collection.find_one({"ident_muestra": "1234567"})["_id"],
                "identificacion": "YY.1234567",
                "color": "Rojo",
                "posicion": 123123,
                "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
            },
            {
                #"paciente_id": collection.find_one({"ident_muestra": "1234567"})["_id"],
                "identificacion": "ZZ.1234567",
                "color": "Verde",
                "posicion": 123123,
                "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
            },
            {
                #"paciente_id": collection.find_one({"ident_muestra": "1234567"})["_id"],
                "identificacion": "kK.1234567",
                "color": "Amarillo",
                "posicion": 123123,
                "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
            },
            {
                #"paciente_id": collection.find_one({"ident_muestra": "2345678"})["_id"],
                "identificacion": "YY.2345678",
                "color": "Azul",
                "posicion": 234234,
                "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
            },
            {
                #"paciente_id": collection.find_one({"ident_muestra": "3456789"})["_id"],
                "identificacion": "YY.3456789",
                "color": "Verde",
                "posicion": 345345,
                "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
            }]
    db_muestras.insert_many(muestras)


    petri = [{
        "identificacion": "1234.112300433",
        "placa": 90,
        "datos_muestra": {
            "tipo": "sangre",
            "fecha": "11/23",
            "hora": "12:00",
            "metodo_siembra": "Vertido",
            "tipo_medio": "Agar sangre",
            "volumen": 5,
            "dilucion": 10,
            "tiempo_incubacion": 4,
            "temperatura": 33
        },
        "datos_imagen": {
            "id_imagen": "imagen1",
            "extension": "jpg",
            "rgb": {
                "r": 255,
                "g": 0,
                "b": 0
            },
            "hsv": {
                "h": 0,
                "s": 100,
                "v": 100
            },
            "resolucion": 1.92,
            "umbral_color": 255
        },
        "datos_analisis": {
            "radio_min": 0.5,
            "radio_max": 5.0
        },
        "resultados": {
            "colonias_placa": 10,
            "colonias_muestra": 5,
            "objetos_no_validos": 2
        }
    },
    {
        "identificacion": "1234.112300433",
        "placa": 90,
        "datos_muestra": {
            "tipo": "sangre",
            "fecha": "11/23",
            "hora": "12:00",
            "metodo_siembra": "Vertido",
            "tipo_medio": "Agar sangre",
            "volumen": 5,
            "dilucion": 10,
            "tiempo_incubacion": 4,
            "temperatura": 33
        },
        "datos_imagen": {
            "id_imagen": "imagen1",
            "extension": "jpg",
            "rgb": {
                "r": 255,
                "g": 0,
                "b": 0
            },
            "hsv": {
                "h": 0,
                "s": 100,
                "v": 100
            },
            "resolucion": 1.92,
            "umbral_color": 255
        },
        "datos_analisis": {
            "radio_min": 0.5,
            "radio_max": 5.0
        },
        "resultados": {
            "colonias_placa": 10,
            "colonias_muestra": 5,
            "objetos_no_validos": 2
        }
    },
    {
        "identificacion": "1234.112300433",
        "placa": 90,
        "datos_muestra": {
            "tipo": "Sangre",
            "fecha": "11/23",
            "hora": "12:00",
            "metodo_siembra": "Vertido",
            "tipo_medio": "Agar sangre",
            "volumen": 5,
            "dilucion": 10,
            "tiempo_incubacion": 4,
            "temperatura": 33
        },
        "datos_imagen": {
            "id_imagen": "imagen1",
            "extension": "jpg",
            "rgb": {
                "r": 255,
                "g": 0,
                "b": 0
            },
            "hsv": {
                "h": 0,
                "s": 100,
                "v": 100
            },
            "resolucion": 1.92,
            "umbral_color": 255
        },
        "datos_analisis": {
            "radio_min": 0.5,
            "radio_max": 5.0
        },
        "resultados": {
            "colonias_placa": 10,
            "colonias_muestra": 5,
            "objetos_no_validos": 2
        }
    },
    {
        "identificacion": "1235.112300434",
        "placa": 91,
        "datos_muestra": {
            "tipo": "orina",
            "fecha": "11/23",
            "hora": "12:30",
            "metodo_siembra": "Vertido",
            "tipo_medio": "Agar MacConkey",
            "volumen": 10,
            "dilucion": 20,
            "tiempo_incubacion": 5,
            "temperatura": 35
        },
        "datos_imagen": {
            "id_imagen": "imagen2",
            "extension": "png",
            "rgb": {
                "r": 0,
                "g": 255,
                "b": 0
            },
            "hsv": {
                "h": 120,
                "s": 100,
                "v": 100
            },
            "resolucion": 1.92,
            "umbral_color": 200
        },
        "datos_analisis": {
            "radio_min": 0.3,
            "radio_max": 4.5
        },
        "resultados": {
            "colonias_placa": 15,
            "colonias_muestra": 8,
            "objetos_no_validos": 1
        }
    },
    {
        "identificacion": "1236.112300435",
        "placa": 92,
        "datos_muestra": {
            "tipo": "saliva",
            "fecha": "11/23",
            "hora": "13:00",
            "metodo_siembra": "Vertido",
            "tipo_medio": "Agar chocolate",
            "volumen": 8,
            "dilucion": 15,
            "tiempo_incubacion": 6,
            "temperatura": 37
        },
        "datos_imagen": {
            "id_imagen": "imagen3",
            "extension": "jpg",
            "rgb": {
                "r": 0,
                "g": 0,
                "b": 255
            },
            "hsv": {
                "h": 240,
                "s": 100,
                "v": 100
            },
            "resolucion": 1.92,
            "umbral_color": 180
        },
        "datos_analisis": {
            "radio_min": 0.2,
            "radio_max": 4.0
        },
        "resultados": {
            "colonias_placa": 20,
            "colonias_muestra": 10,
            "objetos_no_validos": 3
        }
    }]

    db_petri.insert_many(petri)

    print('Datos de prueba añadidos exitosamente')