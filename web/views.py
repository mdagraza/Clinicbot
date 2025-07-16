import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId
from datetime import datetime
from db_connection import *
from panel.decorators import *
from django.conf import settings
import requests

# Conectar con MongoDB
db_pacientes = get_db_pacientes()
db_muestras = get_db_muestras()
db_petri = get_db_petri()

def home(request):
    if request.user:
        print("Usuario autenticado:", request.user["username"])
        print("Id del usuario:", request.user.get("idUsuario"))
    return render(request, "home.html")

# Vista para mostrar la lista de pacientes y el formulario de edición
@login_required
def datos_pacientes(request):
    if request.method == "POST":
        # Obtener los datos del formulario para actualizar un paciente
        paciente_id = request.POST.get("paciente_id")
        nombre = request.POST.get("nombre")
        apellidos = request.POST.get("apellidos")
        ident_muestra = request.POST.get("ident_muestra")
        ident_petri = request.POST.get("ident_petri")
        edad = request.POST.get("edad")
        email = request.POST.get("email")
        genero = request.POST.get("genero")
        gr_sanguineo = request.POST.get("gr_sanguineo")
        
        # Actualizar los datos en MongoDB
        if not paciente_id: #Si no hay ningún paciente cargado, se crea un nuevo con los datos | not... si es none, null o vacio
            nuevo_paciente = {
                "nombre": nombre,
                "apellidos": apellidos,
                "ident_muestra": ident_muestra,
                "ident_petri": ident_petri,
                "edad": int(edad),
                "email": email,
                "genero": genero,
                "gr_sanguineo": gr_sanguineo
            }
            db_pacientes.insert_one(nuevo_paciente)
        else:
            db_pacientes.update_one(
                {"_id": ObjectId(paciente_id)},
                {"$set": {"nombre": nombre, "apellidos": apellidos, "ident_muestra": ident_muestra, "ident_petri": ident_petri, "edad": int(edad), "email": email, "genero": genero, "gr_sanguineo": gr_sanguineo}}
            )
        return redirect('datos_pacientes')
    
    print(f"Hora actual 1: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # Obtener la lista de pacientes a través de API REST
    api_url = f"{settings.API_URL}/api/pacientes" #pacientes-list
    headers = {
        'Authorization': 'Bearer 992457924e83931b3878b0407a2b3694b02a13abb24794ec7f37dba9f8347049' # REVISAR: Cambiar por el token de acceso del usuario autenticado
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        pacientes = response.json()
    else:
        print("Error al obtener los pacientes:", response.status_code, response.text)
        pacientes = []

    print(f"Hora actual 2: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    #print("Pacientes obtenidos:", pacientes)


    # Obtener la lista de pacientes de MongoDB y se ordenan en ascendente (-1 descendente)
    #pacientes = db_pacientes.find().sort("apellidos",1)
    
    # Renombrar _id a id para que no cause problemas en la plantilla
    #pacientes = [{"id": str(paciente["_id"]), "nombre": paciente["nombre"], "edad": paciente["edad"], "email": paciente["email"], "genero": paciente["genero"], "gr_sanguineo": paciente["gr_sanguineo"]} for paciente in pacientes]
    pacientes = [
    {
        "id": str(paciente["_id"]),
        "nombre": paciente.get("nombre", ""), #Si no encuentra la key, se asigna un valor por defecto a la variable
        "apellidos": paciente.get("apellidos", ""),
        "ident_muestra": paciente.get("ident_muestra", ""),
        "ident_petri": paciente.get("ident_petri", ""),
        "edad": paciente.get("edad", ""),
        "email": paciente.get("email", ""),
        "genero": paciente.get("genero", ""),
        "gr_sanguineo": paciente.get("gr_sanguineo", "")
    }
    for paciente in pacientes
    ]

    # Información para la imagen
    data_image = {
        'IMAGE_URLBASE' : settings.MEDIA_URL 
    }

    print(f"Hora actual 3: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # Renderizar la página con la lista de pacientes y el formulario de edición
    return render(request, "pacientes.html", {"pacientes": pacientes, "data_image" : data_image})

def borrar_paciente(request):
    if request.method == 'POST':
        paciente_id = request.POST.get("paciente_id2")
        try:
            # Convierte el ID en ObjectId y elimina el paciente
            resultado = db_pacientes.delete_one({"_id": ObjectId(paciente_id)})

            # Verifica si realmente se eliminó un documento
            if resultado.deleted_count > 0:
                return redirect('datos_pacientes') 
            else:
                return HttpResponse("Persona no encontrada", status=404)
        except Exception as e:
            return redirect('datos_pacientes') 
            #return HttpResponse(f"Error eliminando paciente: {str(e)}", status=500)

    #return HttpResponse("Page not found", status=404)
    raise Http404

@solo_superusuarios
def editar_muestra(request):
    if request.method == "POST":
        # Obtener los datos del formulario para actualizar un paciente
        muestra_id = request.POST.get("muestra_id")
        paciente_id = request.POST.get("paciente_id")
        identificador = request.POST.get("identificador")
        color = request.POST.get("color")
        posicion = request.POST.get("posicion")
        fecha = request.POST.get("fecha")

        print("Datos recibidos:", muestra_id, paciente_id, identificador, color, posicion, fecha)
        
        # Actualizar los datos en MongoDB
        if not muestra_id: #Si no hay ningún paciente cargado, se crea un nuevo con los datos | not... si es none, null o vacio
            print("Creando nueva muestra")
            nueva_muestra = {
                "paciente_id": ObjectId(paciente_id),
                "identificador": identificador,
                "color": color,
                "posicion": posicion,
                #"fecha": fecha,
                "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
            }
            db_muestras.insert_one(nueva_muestra)
        else:
            db_muestras.update_one(
                {"_id": ObjectId(muestra_id)},
                {"$set": {"paciente_id": ObjectId(paciente_id), "identificador": identificador, "color": color, "posicion": posicion, "fecha": fecha}}
            )
        #return redirect('editar_muestra')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    #Obtener la lista de pacientes
    pacientes = db_pacientes.find().sort("apellidos",1)
    pacientes = [
    {
        "id": str(paciente["_id"]),
        "nombre": paciente.get("nombre", ""), #Si no encuentra la key, se asigna un valor por defecto a la variable
        "apellidos": paciente.get("apellidos", ""),
        "edad": paciente.get("edad", ""),
        "email": paciente.get("email", ""),
        "genero": paciente.get("genero", ""),
        "gr_sanguineo": paciente.get("gr_sanguineo", "")
    }
    for paciente in pacientes
    ]


    # Obtener la lista muestras
    muestras = db_muestras.find()
    muestras = [
    {
        "id": str(muestra["_id"]),
        "paciente_id": muestra.get("paciente_id", ""),
        "identificador": muestra.get("identificador", ""), #Si no encuentra la key, se asigna un valor por defecto a la variable
        "color": muestra.get("color", ""),
        "posicion": muestra.get("posicion", ""),
        "fecha": muestra.get("fecha", ""),
    }
    for muestra in muestras
    ]


    # Renderizar la página con la lista de pacientes y el formulario de edición
    return render(request, "muestras.html", {"muestras": muestras, "pacientes": pacientes})


def borrar_muestra(request):
    if request.method == 'POST':
        muestra_id = request.POST.get("muestra_id2")
        try:
            # Convierte el ID en ObjectId y elimina el paciente
            resultado = db_muestras.delete_one({"_id": ObjectId(muestra_id)})

            # Verifica si realmente se eliminó un documento
            if resultado.deleted_count > 0:
                return redirect('editar_muestra') 
            else:
                return HttpResponse("Persona no encontrada", status=404)
        except Exception as e:
            return redirect('editar_muestra') 
            #return HttpResponse(f"Error eliminando paciente: {str(e)}", status=500)

    #return HttpResponse("Page not found", status=404)
    raise Http404

def obtener_muestras(request, identificador_paciente):
    try:        
        patron_id_paciente = {"$regex" : f"{identificador_paciente}$"} # Se convierte el id a un patron que busca solo el string pasado solo en la parte derecha ($ Significa final del string)
        # Filtrar solo las muestras del paciente en MongoDB
        muestras = db_muestras.find({"identificador": patron_id_paciente})
        
        # Convertir los datos a una lista con los IDs como strings
        muestras_lista = [
        {
            "id": str(muestra["_id"]),
            "identificador": muestra.get("identificador", ""), 
            "color": muestra.get("color", ""),
            "posicion": muestra.get("posicion", ""),
            "fecha": muestra.get("fecha", ""),
        }
        for muestra in muestras
        ]
        
        # Devolver los datos en formato JSON
        return JsonResponse(muestras_lista, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def obtener_petri(request, identificador_paciente):
    try:        
        patron_id_paciente = {"$regex": f"^{identificador_paciente[:4]}"} # Se convierte el id a un patron que busca solo el string de los primeros 4 caracteres (^ Significa inicio del string)
        # Filtrar solo las placas petri del paciente en MongoDB
        petri = db_petri.find({"identificador": patron_id_paciente})
        
        # Convertir los datos a una lista con los IDs como strings
        petri_lista = [
        {
            "id": str(p["_id"]),
            "identificador": p.get("identificador", ""), 
            "placa": p.get("placa", ""),
            "datos_muestra": {
                "tipo": p.get("datos_muestra", {}).get("tipo", ""),
                "fecha": p.get("datos_muestra", {}).get("fecha", ""),
                "hora": p.get("datos_muestra", {}).get("hora", ""),
                "metodo_siembra": p.get("datos_muestra", {}).get("metodo_siembra", ""),
                "tipo_medio": p.get("datos_muestra", {}).get("tipo_medio", ""),
                "volumen": p.get("datos_muestra", {}).get("volumen", ""),
                "dilucion": p.get("datos_muestra", {}).get("dilucion", ""),
                "tiempo_incubacion": p.get("datos_muestra", {}).get("tiempo_incubacion", ""),
                "temperatura": p.get("datos_muestra", {}).get("temperatura", "")
            },
            "datos_imagen": {
                "id_imagen": p.get("datos_imagen", {}).get("id_imagen", ""),
                "extension": p.get("datos_imagen", {}).get("extension", ""),
                "rgb": {
                    "r": p.get("datos_imagen", {}).get("rgb", {}).get("r", ""),
                    "g": p.get("datos_imagen", {}).get("rgb", {}).get("g", ""),
                    "b": p.get("datos_imagen", {}).get("rgb", {}).get("b", "")
                },
                "hsv": {
                    "h": p.get("datos_imagen", {}).get("hsv", {}).get("h", ""),
                    "s": p.get("datos_imagen", {}).get("hsv", {}).get("s", ""),
                    "v": p.get("datos_imagen", {}).get("hsv", {}).get("v", "")
                },
                "resolucion": p.get("datos_imagen", {}).get("resolucion", ""),
                "umbral_color": p.get("datos_imagen", {}).get("umbral_color", "")
            },
            "datos_analisis": {
                "radio_min": p.get("datos_analisis", {}).get("radio_min", ""),
                "radio_max": p.get("datos_analisis", {}).get("radio_max", "")
            },
            "resultados": {
                "colonias_placa": p.get("resultados", {}).get("colonias_placa", ""),
                "colonias_muestra": p.get("resultados", {}).get("colonias_muestra", ""),
                "objetos_no_validos": p.get("resultados", {}).get("objetos_no_validos", "")
            },
        }
        for p in petri
        ]
        
        # Devolver los datos en formato JSON
        return JsonResponse(petri_lista, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def borrar_petri(request):
    if request.method == 'POST':
        muestra_id = request.POST.get("muestra_id2")
        try:
            # Convierte el ID en ObjectId y elimina el paciente
            resultado = db_muestras.delete_one({"_id": ObjectId(muestra_id)})

            # Verifica si realmente se eliminó un documento
            if resultado.deleted_count > 0:
                return redirect('editar_muestra') 
            else:
                return HttpResponse("Persona no encontrada", status=404)
        except Exception as e:
            return redirect('editar_muestra') 
            #return HttpResponse(f"Error eliminando paciente: {str(e)}", status=500)

    #return HttpResponse("Page not found", status=404)
    raise Http404

@solo_superusuarios
def editar_petri(request):
    if request.method == "POST":
        # Obtener los datos del formulario para actualizar un paciente
        muestra_id = request.POST.get("muestra_id")
        paciente_id = request.POST.get("paciente_id")
        identificador = request.POST.get("identificador")
        color = request.POST.get("color")
        posicion = request.POST.get("posicion")
        fecha = request.POST.get("fecha")

        print("Datos recibidos:", muestra_id, paciente_id, identificador, color, posicion, fecha)
        
        # Actualizar los datos en MongoDB
        if not muestra_id: #Si no hay ningún paciente cargado, se crea un nuevo con los datos | not... si es none, null o vacio
            print("Creando nueva muestra")
            nueva_muestra = {
                "paciente_id": ObjectId(paciente_id),
                "identificador": identificador,
                "color": color,
                "posicion": posicion,
                #"fecha": fecha,
                "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
            }
            db_muestras.insert_one(nueva_muestra)
        else:
            db_muestras.update_one(
                {"_id": ObjectId(muestra_id)},
                {"$set": {"paciente_id": ObjectId(paciente_id), "identificador": identificador, "color": color, "posicion": posicion, "fecha": fecha}}
            )
        #return redirect('editar_muestra')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    #Obtener la lista de pacientes
    pacientes = db_pacientes.find().sort("apellidos",1)
    pacientes = [
    {
        "id": str(paciente["_id"]),
        "nombre": paciente.get("nombre", ""), #Si no encuentra la key, se asigna un valor por defecto a la variable
        "apellidos": paciente.get("apellidos", ""),
        "edad": paciente.get("edad", ""),
        "email": paciente.get("email", ""),
        "genero": paciente.get("genero", ""),
        "gr_sanguineo": paciente.get("gr_sanguineo", "")
    }
    for paciente in pacientes
    ]


    # Obtener la lista muestras
    muestras = db_muestras.find()
    muestras = [
    {
        "id": str(muestra["_id"]),
        "paciente_id": muestra.get("paciente_id", ""),
        "identificador": muestra.get("identificador", ""), #Si no encuentra la key, se asigna un valor por defecto a la variable
        "color": muestra.get("color", ""),
        "posicion": muestra.get("posicion", ""),
        "fecha": muestra.get("fecha", ""),
    }
    for muestra in muestras
    ]


    # Renderizar la página con la lista de pacientes y el formulario de edición
    return render(request, "muestras.html", {"muestras": muestras, "pacientes": pacientes})



'''

 Datos de persona (Nombre, Apellidos, Edad, Genero, grupo sanguineo)
 Datos de muestra (Identificador(Formato: XY.1234567 [2 primeros caracteres es tipo de análisis, 7 siguientes caracteres es el identificador de la muestra]), color, posicion)
 Datos petri: Identificador: PPPP.ddmmtttTT (PPPP identificador de paciente, dd día, mm mes, ttt horas, TT temperatura)
 
'''