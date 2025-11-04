import requests
from django.conf import settings

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