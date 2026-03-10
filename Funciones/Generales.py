import requests
from django.conf import settings
from bson import ObjectId
from db_connection import MongoDBConnection
mongo = MongoDBConnection()

def peticion_datos(user_id, peticion):
    # Obtener la lista de la peticion a través de API REST
    api_url = f"{settings.API_URL}/api/{peticion}"
    headers = {
        'Authorization': f'Interno {user_id}' 
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener los datos de {peticion}:", response.status_code, response.text)
        return []
    
def peticion_datos_detalle(user_id, peticion, id):
    # Obtener la lista de la peticion a través de API REST
    api_url = f"{settings.API_URL}/api/{peticion}/{id}" 
    headers = {
        'Authorization': f'Interno {user_id}' 
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener los datos de {peticion} con id {id}:", response.status_code, response.text)
        return []
    
def guardar_datos(user_id, peticion, json):
    api_url = f"{settings.API_URL}/api/{peticion}/"
    headers = {
        'Authorization': f'Interno {user_id}' 
    }
    response = requests.post(api_url, json=json, headers=headers)

    if response.status_code == 201 or response.status_code == 200:
        return True
    else:
        print(f"Error al guardar los datos de {peticion}:", response.status_code, response.text)
        return False

def actualizar_datos(user_id, peticion, id, json):
    api_url = f"{settings.API_URL}/api/{peticion}/{id}/"
    headers = {
        'Authorization': f'Interno {user_id}' 
    }
    response = requests.put(api_url, json=json, headers=headers)

    if response.status_code == 201 or response.status_code == 200:
        return True
    else:
        print(f"Error al actualizar los datos de {peticion} del id {id}:", response.status_code, response.text)
        return False
    
def eliminar_datos(user_id, peticion, id):
    api_url = f"{settings.API_URL}/api/{peticion}/{id}/"
    headers = {
        'Authorization': f'Interno {user_id}' 
    }
    response = requests.delete(api_url, headers=headers)

    if response.status_code == 200 or response.status_code == 202:
        return True
    else:
        print(f"Error al eliminar los datos de {peticion} del id {id}:", response.status_code, response.text)
        return False

def get_tipo_usuario(header):
    #Usuario Interno
    if header.startswith('Interno '):
        user_id = header.split(' ')[1]

    #Token bearer
    if header.startswith('Bearer '):
        token = header.split(' ')[1]
        user_id = str(mongo.get_collection_db_usuarios('api_tokens').find_one(
            {"token": token},
            {"_id":0, "user_id":1}
            ).get("user_id"))
        
    #Devolver el tipo de usuario
    return mongo.get_collection_db_usuarios().find_one(
            {"_id": ObjectId(user_id)},
            {"_id":0, "permisos":1}
            ).get("permisos")[0]