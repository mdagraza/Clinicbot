import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId
from datetime import datetime
from db_connection import *
from panel.decorators import *

# Conectar con MongoDB
collection = get_db_pacientes()
collection2 = get_db_muestras()

def home2(request):
    if request.user:
        print("Usuario autenticado:", request.user["username"])
        print("Id del usuario:", request.user.get("idUsuario"))
    return render(request, "home2.html")

# Vista para mostrar la lista de usuarios y el formulario de edición
@login_required
def editar_usuario(request):
    if request.method == "POST":
        # Obtener los datos del formulario para actualizar un usuario
        usuario_id = request.POST.get("usuario_id")
        nombre = request.POST.get("nombre")
        apellidos = request.POST.get("apellidos")
        ident_paciente = request.POST.get("ident_paciente")
        edad = request.POST.get("edad")
        email = request.POST.get("email")
        genero = request.POST.get("genero")
        gr_sanguineo = request.POST.get("gr_sanguineo")
        
        # Actualizar los datos en MongoDB
        if not usuario_id: #Si no hay ningún usuario cargado, se crea un nuevo con los datos | not... si es none, null o vacio
            nuevo_usuario = {
                "nombre": nombre,
                "apellidos": apellidos,
                "ident_paciente": ident_paciente,
                "edad": int(edad),
                "email": email,
                "genero": genero,
                "gr_sanguineo": gr_sanguineo
            }
            collection.insert_one(nuevo_usuario)
        else:
            collection.update_one(
                {"_id": ObjectId(usuario_id)},
                {"$set": {"nombre": nombre, "apellidos": apellidos, "ident_paciente": ident_paciente, "edad": int(edad), "email": email, "genero": genero, "gr_sanguineo": gr_sanguineo}}
            )
        return redirect('editar_usuario')
    
    # Obtener la lista de usuarios de MongoDB y se ordenan en ascendente (-1 descendente)
    usuarios = collection.find().sort("apellidos",1)
    
    # Renombrar _id a id para que no cause problemas en la plantilla
    #usuarios = [{"id": str(usuario["_id"]), "nombre": usuario["nombre"], "edad": usuario["edad"], "email": usuario["email"], "genero": usuario["genero"], "gr_sanguineo": usuario["gr_sanguineo"]} for usuario in usuarios]
    usuarios = [
    {
        "id": str(usuario["_id"]),
        "nombre": usuario.get("nombre", ""), #Si no encuentra la key, se asigna un valor por defecto a la variable
        "apellidos": usuario.get("apellidos", ""),
        "ident_paciente": usuario.get("ident_paciente", ""),
        "edad": usuario.get("edad", ""),
        "email": usuario.get("email", ""),
        "genero": usuario.get("genero", ""),
        "gr_sanguineo": usuario.get("gr_sanguineo", "")
    }
    for usuario in usuarios
    ]


    # Renderizar la página con la lista de usuarios y el formulario de edición
    return render(request, "pacientes.html", {"usuarios": usuarios})

def borrar_usuario(request):
    if request.method == 'POST':
        usuario_id = request.POST.get("usuario_id2")
        try:
            # Convierte el ID en ObjectId y elimina el usuario
            resultado = collection.delete_one({"_id": ObjectId(usuario_id)})

            # Verifica si realmente se eliminó un documento
            if resultado.deleted_count > 0:
                return redirect('editar_usuario') 
            else:
                return HttpResponse("Persona no encontrada", status=404)
        except Exception as e:
            return redirect('editar_usuario') 
            #return HttpResponse(f"Error eliminando usuario: {str(e)}", status=500)

    #return HttpResponse("Page not found", status=404)
    raise Http404

@solo_superusuarios
def editar_muestra(request):
    if request.method == "POST":
        # Obtener los datos del formulario para actualizar un usuario
        muestra_id = request.POST.get("muestra_id")
        paciente_id = request.POST.get("paciente_id")
        identificador = request.POST.get("identificador")
        color = request.POST.get("color")
        posicion = request.POST.get("posicion")
        fecha = request.POST.get("fecha")

        print("Datos recibidos:", muestra_id, paciente_id, identificador, color, posicion, fecha)
        
        # Actualizar los datos en MongoDB
        if not muestra_id: #Si no hay ningún usuario cargado, se crea un nuevo con los datos | not... si es none, null o vacio
            print("Creando nueva muestra")
            nueva_muestra = {
                "paciente_id": ObjectId(paciente_id),
                "identificador": identificador,
                "color": color,
                "posicion": posicion,
                #"fecha": fecha,
                "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
            }
            collection2.insert_one(nueva_muestra)
        else:
            collection2.update_one(
                {"_id": ObjectId(muestra_id)},
                {"$set": {"paciente_id": ObjectId(paciente_id), "identificador": identificador, "color": color, "posicion": posicion, "fecha": fecha}}
            )
        #return redirect('editar_muestra')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    #Obtener la lista de usuarios
    usuarios = collection.find().sort("apellidos",1)
    usuarios = [
    {
        "id": str(usuario["_id"]),
        "nombre": usuario.get("nombre", ""), #Si no encuentra la key, se asigna un valor por defecto a la variable
        "apellidos": usuario.get("apellidos", ""),
        "edad": usuario.get("edad", ""),
        "email": usuario.get("email", ""),
        "genero": usuario.get("genero", ""),
        "gr_sanguineo": usuario.get("gr_sanguineo", "")
    }
    for usuario in usuarios
    ]


    # Obtener la lista muestras
    muestras = collection2.find()
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


    # Renderizar la página con la lista de usuarios y el formulario de edición
    return render(request, "muestras.html", {"muestras": muestras, "usuarios": usuarios})


def borrar_muestra(request):
    if request.method == 'POST':
        muestra_id = request.POST.get("muestra_id2")
        try:
            # Convierte el ID en ObjectId y elimina el usuario
            resultado = collection2.delete_one({"_id": ObjectId(muestra_id)})

            # Verifica si realmente se eliminó un documento
            if resultado.deleted_count > 0:
                return redirect('editar_muestra') 
            else:
                return HttpResponse("Persona no encontrada", status=404)
        except Exception as e:
            return redirect('editar_muestra') 
            #return HttpResponse(f"Error eliminando usuario: {str(e)}", status=500)

    #return HttpResponse("Page not found", status=404)
    raise Http404

def obtener_muestras(request, identificador_paciente):
    try:        
        patron_id_paciente = {"$regex" : f"{identificador_paciente}$"} # Se convierte el id a un patron que busca solo el string pasado solo en la parte derecha ($ Significa final del string)
        # Filtrar solo las muestras del paciente en MongoDB
        muestras = collection2.find({"identificador": patron_id_paciente})
        
        # Convertir los datos a una lista con los IDs como strings
        muestras_lista = [
        {
            "id": str(muestra["_id"]),
            "paciente_id": str(muestra.get("paciente_id", "")),
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

        # Devolver los datos en formato JSON
        return JsonResponse('', safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




'''

 Datos de persona (Nombre, Apellidos, Edad, Genero, grupo sanguineo)
 Datos de muestra (Identificador(Formato: XY.1234567 [2 primeros caracteres es tipo de análisis, 7 siguientes caracteres es el identificador de la muestra]), color, posicion)
 Datos petri: Identificador: PPPP.ddmmtttTT (PPPP identificador de paciente, dd día, mm mes, ttt horas, TT temperatura)
 
'''