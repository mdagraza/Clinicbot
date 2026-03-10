from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson.objectid import ObjectId
from db_connection import MongoDBConnection
import re
from datetime import datetime, timezone
from api.decorators import token_required

from Funciones.Generales import get_tipo_usuario
from api.schemas.schemas import muestras_schema
from api.schemas.validator import validate_json

from drf_spectacular.utils import extend_schema

PATRON_CODE = r"^[a-zA-Z0-9]{4}\.[0-9]{9}$"

mongo = MongoDBConnection()

################### GESTION MUESTRAS SANGRE ##################        
class ItemListView_Muestras(APIView):
    """
    Endpoint de la API para gestionar registros de muestras de sangre.
    
    Listar y crear muestras de sangre. Requiere autenticación por token.
    El acceso a las muestras se filtra según el tipo de usuario.
    """
    def __init__(self):
        self.collection = mongo.get_collection_db_muestras()
    
    @token_required
    def get(self, request):
        """
        Obtener todas las muestras de eritrocitos de sangre.
        
        Devuelve una lista en formato JSON de todas las muestras de sangre.
        """
        #Devolver muestras según usuario
        tipo_usuario = get_tipo_usuario(request.META.get('HTTP_AUTHORIZATION', ''))

        if(tipo_usuario == "superuser"):
            items = list(self.collection.find())
        else:
            items = list(self.collection.find({"datos_recepcion.tipo_usuario": tipo_usuario}))
        # Convertir ObjectId a string para poder serializar a JSON
        for item in items:
            item['_id'] = str(item['_id'])
            # Verificar si existe paciente_id antes de convertirlo
            if 'paciente_id' in item and item['paciente_id'] is not None:
                item['paciente_id'] = str(item['paciente_id'])
        return Response(items)
    
    @token_required
    def post(self, request):
        """
        Crear un nuevo registro de muestra de eritrocitos de sangre.
        
        Crea una nueva muestra de sangre con datos validados y un código de identificación único.<br/>
        Identificación esperada en JSON: PPPP.123456789
        """
        data = request.data

        #Filtrar entrada del codigo
        if "identificacion" not in data or not re.match(PATRON_CODE, data["identificacion"]):
            return Response({"error": "La identificación no es válida. Patrón esperado: AAAA.123456789"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar si ya existe en la base de datos
        if self.collection.find_one({"identificacion": data["identificacion"]}):
            return Response({"error": f"Ya existe un registro con la identificación: {str(data['identificacion'])}"}, status=status.HTTP_409_CONFLICT)

        # Agregar datos extra
        data["datos_recepcion"] = {
            "fecha": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tipo_usuario": get_tipo_usuario(
                request.META.get('HTTP_AUTHORIZATION', '')
            )
        }

        result = self.collection.insert_one(data)
        if(result):
            return Response({f"Registro con la identificación {str(data['identificacion'])} guardada."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error al guardar en la base de datos."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          

class ItemDetailView_Muestras(APIView):
    def __init__(self):
        self.collection = mongo.get_collection_db_muestras()
    
    # GET para obtener un item específico
    @token_required
    def get(self, request, id):
        """
        Obtener uno o varios registros de muestra de eritrocitos de sangre.
        
        Devuelve una lista en formato JSON de todas una o varias muestras de sangre.<br/>
        Identificación esperada : PPPP (Identificación de paciente)<br/>
        Identificación esperada: PPPP.123456789 (Identificación de la muestra)
        """
        try:
            patron_id_paciente = {"$regex" : f"^{id}"} # Se convierte el id a un patron que busca solo el string de los primeros 4 caracteres
            tipo_usuario = get_tipo_usuario(request.META.get('HTTP_AUTHORIZATION', ''))

            #Se busca por la identificacion del paciente
            if(tipo_usuario == "superuser"):
                items = list(self.collection.find({"identificacion": patron_id_paciente}))
            else:
                items = list(self.collection.find({"identificacion": patron_id_paciente, "datos_recepcion.tipo_usuario": tipo_usuario}))

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
    @token_required
    def put(self, request, id):
        """
        Actualizar un registro de muestra de eritrocitos de sangre.
        
        Actualiza los valores de un registro de muestra de sangre.<br/>
        Identificación esperada: PPPP.123456789 (Identificación de la muestra)
        """
        try: 
            registro = self.collection.find_one({"identificacion": id})

            if not registro:
                return Response(
                    {"error": "Muestra no encontrada"},
                    status=status.HTTP_404_NOT_FOUND
                )

            data = request.data

            #TODO : Filtrar los campos

            result = self.collection.update_one(
                {"_id": registro["_id"]},
                {"$set": data}
            )
            if result.modified_count:
                return Response({"message": "Actualizado correctamente"})
            return Response({"error": "Ningún registro modificado respecto al original"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE para eliminar un item
    @extend_schema(exclude=True)
    @token_required
    def delete(self, request, id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(id)})
            if result.deleted_count:
                return Response({"message": "Eliminado correctamente"})
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(exclude=True)
class ItemListView_MuestrasNoAsociadas(APIView):
    def __init__(self):
        self.collection = mongo.get_collection_db_muestras()
        self.collection_pacientes = mongo.get_collection_db_pacientes()
    
    # GET para obtener todos los items
    @token_required
    def get(self, request):
        try:
            tipo_usuario = get_tipo_usuario(request.META.get('HTTP_AUTHORIZATION', ''))

            #Obtener identificaciones de todos los pacientes
            pacientes = list(self.collection_pacientes.find())
            list_ids = [paciente["ident_muestra"] for paciente in pacientes if "ident_muestra" in paciente and paciente["datos_recepcion"]["tipo_usuario"]==tipo_usuario]

            exclusiones = [
                {"identificacion": {"$regex": f"^{id}"}}
                for id in list_ids
            ]

            #Se busca por la identificacion del paciente
            if(tipo_usuario == "superuser"):
                items = list(self.collection.find({"$nor": exclusiones}))
            else:
                items = list(self.collection.find({"$nor": exclusiones, "datos_recepcion.tipo_usuario": tipo_usuario}))

            if items:
                # Convertir ObjectId a string para poder serializar a JSON
                for item in items:
                    item['_id'] = str(item['_id'])
                    # Verificar si existe paciente_id antes de convertirlo
                    if 'paciente_id' in item and item['paciente_id'] is not None:
                        item['paciente_id'] = str(item['paciente_id'])
                return Response(items)
            return Response({"error": "No encontrado ningún dato no relacionado a ningún paciente"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)