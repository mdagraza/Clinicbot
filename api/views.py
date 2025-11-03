from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson.objectid import ObjectId
from db_connection import MongoDBConnection
import re
from datetime import datetime
from panel.decorators import *
from .tokens import TokenManager
from Clinicbot.utils import UsuarioService
from .decorators import token_required

import os
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import uuid

PATRON_CODE = r"^[a-zA-Z0-9]{2}\.[a-zA-Z0-9]{7}$"

mongo = MongoDBConnection()

class ItemListView_Pacientes(APIView):
    def __init__(self):
        self.collection = mongo.get_collection_db_pacientes()
    
    # GET para obtener todos los items
    @token_required
    def get(self, request):
        items = list(self.collection.find().sort("apellidos",1)) # Ordenar por apellidos en orden ascendente
        # Convertir ObjectId a string para poder serializar a JSON
        for item in items:
            item['_id'] = str(item['_id'])
        return Response(items)
    
    # POST para crear un nuevo item
    def post(self, request):
        data = request.data
        result = self.collection.insert_one(data)
        return Response({"id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)

class ItemDetailView_Pacientes(APIView):
    def __init__(self):
        self.collection = mongo.get_collection_db_pacientes()
    
    # GET para obtener un item específico
    def get(self, request, id):
        try:
            item = self.collection.find_one({"_id": ObjectId(id)})
            if item:
                item['_id'] = str(item['_id'])
                return Response(item)
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # PUT para actualizar un item
    def put(self, request, id):
        try:
            data = request.data
            result = self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": data}
            )
            if result.modified_count:
                return Response({"message": "Actualizado correctamente"})
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE para eliminar un item
    def delete(self, request, id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(id)})
            if result.deleted_count:
                return Response({"message": "Eliminado correctamente"})
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

################### GESTION MUESTRAS SANGRE ##################        
class ItemListView_Muestras(APIView):
    def __init__(self):
        self.collection = mongo.get_collection_db_muestras()
    
    # GET para obtener todos los items
    @token_required
    def get(self, request):
        items = list(self.collection.find())
        # Convertir ObjectId a string para poder serializar a JSON
        for item in items:
            item['_id'] = str(item['_id'])
            # Verificar si existe paciente_id antes de convertirlo
            if 'paciente_id' in item and item['paciente_id'] is not None:
                item['paciente_id'] = str(item['paciente_id'])
        return Response(items)
    
    # POST para crear un nuevo item
    @token_required
    def post(self, request):
        data = request.data

        #Filtrar entrada del codigo
        if "identificacion" not in data or not re.match(PATRON_CODE, data["identificacion"]):
            return Response({"error": "La identificación(AA.1234567) no es válida."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar si ya existe en la base de datos
        if self.collection.find_one({"identificacion": data["identificacion"]}):
            return Response({"error": f"Ya existe un registro con la identificación: {str(data['identificacion'])}"}, status=status.HTTP_400_BAD_REQUEST)


        # Agregar la fecha
        data["fecha"] = datetime.now().strftime("%Y-%m-%dT%H:%M")

        result = self.collection.insert_one(data)
        return Response({"id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)

class ItemDetailView_Muestras(APIView):
    def __init__(self):
        self.collection = mongo.get_collection_db_muestras()
    
    # GET para obtener un item específico
    def get(self, request, id):
        try:
            patron_id_paciente = {"$regex" : f"{id}$"} # Se convierte el id a un patron que busca solo el string de los últimos caracteres
            items = list(self.collection.find({"identificacion": patron_id_paciente})) # Se busca por la identificacion del paciente

            if items:
                # Convertir ObjectId a string para poder serializar a JSON
                for item in items:
                    item['_id'] = str(item['_id'])
                    # Verificar si existe paciente_id antes de convertirlo
                    if 'paciente_id' in item and item['paciente_id'] is not None:
                        item['paciente_id'] = str(item['paciente_id'])
                return Response(items)
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # PUT para actualizar un item
    def put(self, request, id):
        try: 
            data = request.data

            #Proteger los campos que puede editar
            campos_permitidos = ['color', 'posicion'] 
            campos_invalidos = [campo for campo in data.keys() if campo not in campos_permitidos]
            if campos_invalidos:
                return Response({
                    "error": f"No se pueden editar los campos: {', '.join(campos_invalidos)}",
                    "Solo se pueden editar los campos:": campos_permitidos
                }, status=400)

            '''# Eliminar campos que no se pueden actualizar
            campos_protegidos = ['identificacion', 'fecha']
            for campo in campos_protegidos:
                if campo in data:
                    data.pop(campo)'''

            result = self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": data}
            )
            if result.modified_count:
                return Response({"message": "Actualizado correctamente"})
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE para eliminar un item
    def delete(self, request, id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(id)})
            if result.deleted_count:
                return Response({"message": "Eliminado correctamente"})
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
################### GESTION PLACAS PETRI ##################
class ItemListView_Petri(APIView):
    def __init__(self):
        self.collection = mongo.get_collection_db_petri()
    
    # GET para obtener todos los items
    @token_required
    def get(self, request):
        items = list(self.collection.find())
        # Convertir ObjectId a string para poder serializar a JSON
        for item in items:
            item['_id'] = str(item['_id'])
            # Verificar si existe paciente_id antes de convertirlo
            if 'paciente_id' in item and item['paciente_id'] is not None:
                item['paciente_id'] = str(item['paciente_id'])
        return Response(items)
    
    # POST para crear un nuevo item
    @token_required
    def post(self, request):
        data = request.data

        '''#Filtrar entrada del codigo
        if "identificacion" not in data or not re.match(PATRON_CODE, data["identificacion"]):
            return Response({"error": "La identificacion(AA.1234567) no es válida."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar si ya existe en la base de datos
        if self.collection.find_one({"identificacion": data["identificacion"]}):
            return Response({"error": f"Ya existe un registro con la identificacion: {str(data['identificacion'])}"}, status=status.HTTP_400_BAD_REQUEST)'''

        # Agregar la fecha
        data["fecha"] = datetime.now().strftime("%Y-%m-%dT%H:%M")

        result = self.collection.insert_one(data)
        return Response({"id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)

class ItemDetailView_Petri(APIView):
    def __init__(self):
        self.collection = mongo.get_collection_db_petri()
    
    # GET para obtener un item específico
    def get(self, request, id):
        try:
            patron_id_paciente = {"$regex" : f"^{id}"} # Se convierte el id a un patron que busca solo el string de los primeros 4 caracteres
            items = list(self.collection.find({"identificacion": patron_id_paciente})) # Se busca por la identificacion del paciente

            if items:
                # Convertir ObjectId a string para poder serializar a JSON
                for item in items:
                    item['_id'] = str(item['_id'])
                    # Verificar si existe paciente_id antes de convertirlo
                    if 'paciente_id' in item and item['paciente_id'] is not None:
                        item['paciente_id'] = str(item['paciente_id'])
                return Response(items)
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # PUT para actualizar un item
    def put(self, request, id):
        try: 
            data = request.data

            #Proteger los campos que puede editar
            '''campos_permitidos = ['color', 'posicion'] 
            campos_invalidos = [campo for campo in data.keys() if campo not in campos_permitidos]
            if campos_invalidos:
                return Response({
                    "error": f"No se pueden editar los campos: {', '.join(campos_invalidos)}",
                    "Solo se pueden editar los campos:": campos_permitidos
                }, status=400)'''

            '''# Eliminar campos que no se pueden actualizar
            campos_protegidos = ['identificacion', 'fecha']
            for campo in campos_protegidos:
                if campo in data:
                    data.pop(campo)'''

            result = self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": data}
            )
            if result.modified_count:
                return Response({"message": "Actualizado correctamente"})
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE para eliminar un item
    def delete(self, request, id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(id)})
            if result.deleted_count:
                return Response({"message": "Eliminado correctamente"})
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

################## GESTION TOKENS ##################
class TokenView(APIView):
    def __init__(self):
        self.users = mongo.get_collection_db_usuarios()
        self.tokens = mongo.get_collection_db_usuarios('api_tokens')
        self.token_manager = TokenManager()
    
    # Endpoint para obtener un token
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        expires = request.data.get('expires') #Debe pasarse en horas
        
        # Verificar credenciales (ajusta esto según tu sistema)
        user = self.users.find_one({"username": username})
        
        if not user or not self.verify_password(username, password):
            return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generar token
        token = self.token_manager.generate_token(str(user['_id']), expires)
        
        return Response({
            "access_token": token,
            "token_type": "Bearer Token",
            "expires_in_hours": expires,
            "date_expires": datetime.fromisoformat(str(self.tokens.find_one({"token": token})["expires_at"])).strftime("%d/%m/%Y %H:%M")
        })
    
    def verify_password(self, u_username, u_password):
        return UsuarioService().autenticar_usuario(u_username, u_password)
    
################ GESTIÓN DE IMAGENES ################
class Save_Images(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    @token_required
    def post(self, request):              
        # Procesar y analizar archivos
        archivos_procesados = []
        errores = []

        for field_name, file_obj in request.FILES.items():         
            # Validar que sea PNG o JPG
            if 'png' not in file_obj.content_type.lower() and 'jpg' not in file_obj.content_type.lower() and 'jpeg' not in file_obj.content_type.lower():
                return Response({'error': f"{file_obj.name}: Solo se permiten archivos PNG, JPG o JPEG"}, status=status.HTTP_400_BAD_REQUEST)
                #break #Se pasa al siguiente archivo

            if file_obj.size > settings.DATA_UPLOAD_MAX_MEMORY_SIZE: 
                return Response({'error': f"La imagen '{file_obj.name}' es demasiado grande. Enviado: {file_obj.size/1048576}MB | Máximo: {settings.DATA_UPLOAD_MAX_MEMORY_SIZE/1048576}MB"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Resetear posición del archivo
                file_obj.seek(0)
                
                # Leer todo el archivo
                full_data = file_obj.read()
                file_obj.seek(0)  # Volver al inicio por si acaso
                
                # Guardar archivo en la carpeta petri
                saved_path = None
                try:
                    # Crear directorio petri si no existe
                    petri_dir = os.path.join(settings.MEDIA_ROOT, 'petri')
                    os.makedirs(petri_dir, exist_ok=True)
                    
                    # Respetar el nombre original del archivo
                    if file_obj.name:
                        filename = file_obj.name
                    else:
                        # Solo si no tiene nombre, generar uno
                        filename = f"archivo_sin_nombre_{uuid.uuid4().hex[:8]}"
                    
                    saved_path = os.path.join(petri_dir, filename)
                    
                    # Si ya existe, agregar número secuencial
                    counter = 1
                    while os.path.exists(saved_path):
                        name, ext = os.path.splitext(filename)
                        saved_path = os.path.join(petri_dir, f"{name}_{counter}{ext}")
                        counter += 1
                    
                    # Guardar el archivo
                    with open(saved_path, 'wb') as f:
                        f.write(full_data)
                    
                except Exception as save_error:
                    print(f"ERROR: API Views: No se pudo guardar el archivo: {save_error}")
                    saved_path = None
                
                # Agregar a la lista de procesados
                archivo_info = {
                    'campo': field_name,
                    'nombre_original': file_obj.name,
                    'nombre_guardado': os.path.basename(saved_path) if saved_path else None,
                    'size_bytes': file_obj.size,
                    'size_kb': round(file_obj.size / 1024, 2),
                    'content_type': file_obj.content_type,
                    'procesado_en': datetime.now().isoformat()
                }
                archivos_procesados.append(archivo_info)
                
            except Exception as e:
                error_msg = f"Error procesando archivo '{field_name}': {str(e)}"
                errores.append(error_msg)
                print(f"ERROR: API Views: {error_msg}")
                import traceback
                traceback.print_exc()
        
        if archivos_procesados:
            return Response({
                "status": "success",
                "mensaje": "Archivos recibidos y procesados correctamente",
                "archivos_procesados": archivos_procesados,
                "total_archivos": len(archivos_procesados),
                "campos_texto": {k: v for k, v in request.data.items() if k not in request.FILES},
                "errores": errores if errores else None,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return Response({
                "status": "error",
                "mensaje": "No se encontraron archivos válidos para procesar",
                "debug_info": {
                    "files_keys": list(request.FILES.keys()),
                    "data_keys": list(request.data.keys()),
                    "content_type": request.content_type,
                    "errores": errores
                },
                "timestamp": datetime.now().isoformat()
            }, status=400)