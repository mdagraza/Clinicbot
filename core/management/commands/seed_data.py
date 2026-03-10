from django.core.management.base import BaseCommand
from datetime import datetime

from db_connection import MongoDBConnection
mongo = MongoDBConnection()

# Comando para crear datos de prueba: python manage.py seed_data <str: username> | El string debe ser el nombre del usuario para crear los datos.
class Command(BaseCommand):
    help = "Crea datos de prueba"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Nombre de usuario")

    def handle(self, *args, **options):
        username = options.get("username")

        #Buscar el usuario
        user = mongo.get_collection_db_usuarios().find_one({"username": username})
        if not user:
            self.stdout.write(f"El usuario '{username}' no existe")
            return
        
        #Obtener id del usuario
        user_permiso = user["permisos"][0]

        #Verificar que los datos no hayan sido creados ya
        if mongo.get_collection_db_pacientes().find_one({"ident_muestra": "7ZZ7", "datos_recepcion.tipo_usuario": user_permiso}):
            self.stdout.write(f"Los datos de prueba ya existen para el usuario '{username}'")
            return
        
        #Crear pacientes
        pacientes = [
        {
          "nombre": "[T] Daniel",
          "apellidos": "Sanchez Pérez",
          "ident_muestra": "7ZZ7",
          "ident_petri": "77Z7",
          "edad": 30,
          "email": "nombre_1@test.com",
          "genero": "Hombre",
          "gr_sanguineo": "A+",
          "datos_recepcion": {
            "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "tipo_usuario": user_permiso
          }
        },
        {
          "nombre": "[T] María Antonia",
          "apellidos": "Zacarias Del Río Parísimo de la Vega Fernandez",
          "ident_muestra": "8Y88",
          "ident_petri": "8H88",
          "edad": 25,
          "email": "nombre_2@test.com",
          "genero": "Mujer",  
          "gr_sanguineo": "B-",
          "datos_recepcion": {
            "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "tipo_usuario": user_permiso
          }
        },
        {
          "nombre": "[T] Alberto",
          "apellidos": "Río Pérez",
          "ident_muestra": "V9V8",
          "ident_petri": "9V88",
          "edad": 18,
          "email": "nombre_3@test.com",
          "genero": "Otro",  
          "gr_sanguineo": "0-",
          "datos_recepcion": {
            "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "tipo_usuario": user_permiso
          }
        }]
        mongo.get_collection_db_pacientes().insert_many(pacientes)

        #Crear muestras
        muestras = [{
            "identificacion": "7ZZ7.112600433",
            "caracteristicas_camara": "Cámara Neubauer digital",
            "datos_muestra": {
                "tipo_muestra": "Sangre venosa",
                "fecha": "03/11",
                "hora": "10:00",
                "metodo_dilucion": "manual",
                "tipo_diluyente": "Buffer fosfato salino",
                "volumen_muestra_sembrado": 0.1,
                "dilucion": 200
            },
            "datos_imagen": {
                "id_imagen": "1",
                "extension": "png",
                "rgb": {
                "r": 220,
                "g": 100,
                "b": 100
                },
                "hsv": {
                "h": 0,
                "s": 0.8,
                "v": 0.9
                },
                "resolucion_imagen": 16,
                "umbral_color": 0.5
            },
            "datos_analisis": {
                "radio_min": 10,
                "radio_max": 50,
                "parametros_procesamiento": "Análisis automático 1-1"
            },
            "resultados": {
                "superficie_contada_1_cuadrado": 0.04,
                "superficie_contada_5_cuadrados": 0.2,
                "profundidad_camara_recuento": 0.1,
                "factor_dilucion": "1/200",
                "eritrocitos_cuadrado_1": 104,
                "eritrocitos_cuadrado_2": 95,
                "eritrocitos_cuadrado_3": 101,
                "eritrocitos_cuadrado_4": 103,
                "eritrocitos_cuadrado_5": 105,
                "eritrocitos_por_muestra": 4567178.826671993,
                "valores_referencia_mujeres": "4.2 a 5.4 millones/mm³",
                "valores_referencia_hombres": "4.7 a 6.1 millones/mm³"
            },
            "datos_recepcion": {
              "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M"),
              "tipo_usuario": user_permiso
            }
        },
        {
            "identificacion": "8Y88.112300435",
            "caracteristicas_camara": "Cámara Neubauer digital",
            "datos_muestra": {
                "tipo_muestra": "Sangre venosa",
                "fecha": "03/11",
                "hora": "10:00",
                "metodo_dilucion": "manual",
                "tipo_diluyente": "Buffer fosfato salino",
                "volumen_muestra_sembrado": 0.1,
                "dilucion": 200
            },
            "datos_imagen": {
                "id_imagen": "1",
                "extension": "png",
                "rgb": {
                "r": 220,
                "g": 100,
                "b": 100
                },
                "hsv": {
                "h": 0,
                "s": 0.8,
                "v": 0.9
                },
                "resolucion_imagen": 16,
                "umbral_color": 0.5
            },
            "datos_analisis": {
                "radio_min": 10,
                "radio_max": 50,
                "parametros_procesamiento": "Análisis automático 1-1"
            },
            "resultados": {
                "superficie_contada_1_cuadrado": 0.04,
                "superficie_contada_5_cuadrados": 0.2,
                "profundidad_camara_recuento": 0.1,
                "factor_dilucion": "1/200",
                "eritrocitos_cuadrado_1": 104,
                "eritrocitos_cuadrado_2": 95,
                "eritrocitos_cuadrado_3": 101,
                "eritrocitos_cuadrado_4": 103,
                "eritrocitos_cuadrado_5": 105,
                "eritrocitos_por_muestra": 4567178.826671993,
                "valores_referencia_mujeres": "4.2 a 5.4 millones/mm³",
                "valores_referencia_hombres": "4.7 a 6.1 millones/mm³"
            },
            "datos_recepcion": {
              "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M"),
              "tipo_usuario": user_permiso
            }
        }]
        mongo.get_collection_db_muestras().insert_many(muestras)

        petri = [
        {
          "identificacion": "77Z7.112300433",
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
          },
          "datos_recepcion": {
            "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "tipo_usuario": user_permiso
          }
        },
        {
          "identificacion": "8H88.112300433",
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
          },
          "datos_recepcion": {
            "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "tipo_usuario": user_permiso
          }
        }]

        mongo.get_collection_db_petri().insert_many(petri)

        self.stdout.write(f"Datos de prueba creados para '{username}'")