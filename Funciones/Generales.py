def peticion_datos(user_id, peticion):
    import requests
    from django.conf import settings

    # Obtener la lista de la peticion a través de API REST
    api_url = f"{settings.API_URL}/api/{peticion}" #pacientes-list
    headers = {
        'Authorization': f'Interno {user_id}' 
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener los datos de {peticion}:", response.status_code, response.text)
        return []