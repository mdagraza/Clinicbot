from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson.objectid import ObjectId
from db_connection import MongoDBConnection
from datetime import datetime, timezone
from api.decorators import token_required

from Funciones.Generales import get_tipo_usuario
from api.schemas.schemas import paciente_schema
from api.schemas.validator import validate_json

from drf_spectacular.utils import extend_schema

PATRON_CODE = r"^[a-zA-Z0-9]{4}\.[0-9]{9}$"

mongo = MongoDBConnection()

################### GESTION PACIENTES ##################    
class ItemListView_Pacientes(APIView):
    """
    Endpoint de la API para gestionar registros de pacientes.
    
    Listar y crear registros de pacientes. Requiere autenticación por token.
    El acceso a los registros de pacientes se filtra según el tipo de usuario.
    """
    def __init__(self):
        self.collection = mongo.get_collection_db_pacientes()
    
    @token_required
    def get(self, request):
        """
        Obtener todas los pacientes.
        
        Devuelve una lista en formato JSON de todas los pacientes.
        """
        #Devolver pacientes según usuario
        tipo_usuario = get_tipo_usuario(request.META.get('HTTP_AUTHORIZATION', ''))

        if(tipo_usuario == "superuser"):
            items = list(self.collection.find().sort("apellidos",1)) # Ordenar por apellidos en orden ascendente
        else:
            items = list(self.collection.find({"datos_recepcion.tipo_usuario": tipo_usuario}).sort("apellidos",1)) # Ordenar por apellidos en orden ascendente
        # Convertir ObjectId a string para poder serializar a JSON
        for item in items:
            item['_id'] = str(item['_id'])
        return Response(items)
    
    @token_required
    def post(self, request):
        """
        Crear un nuevo paciente.
        
        Crea un nuevo paciente con datos validados y un código de identificación único.<br/>
        Identificación esperada en JSON: PPPP
        """
        data = request.data

        #TODO: Comprobar que no haya ningun identificador repetido [ident_petri | ident_muestra]

        # Filtrar json
        valid, errors, warnings = validate_json(paciente_schema, data)

        if not valid:
            return Response(
                {"error": "Datos inválidos", "detalles": errors, "avisos": warnings},
                status=status.HTTP_400_BAD_REQUEST
            )            

        # Agregar datos extra
        data["datos_recepcion"] = {
            "fecha": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tipo_usuario": get_tipo_usuario(
                request.META.get('HTTP_AUTHORIZATION', '')
            )
        }

        result = self.collection.insert_one(data)
        if(result):
            return Response({"mensaje":f"Paciente {str(data['nombre'])} {str(data['apellidos'])} guardado.","avisos": warnings}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error al guardar en la base de datos."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ItemDetailView_Pacientes(APIView):
    """
    Endpoint de la API para consultar, actualizar y eliminar registros individuales de pacientes.
    """
    def __init__(self):
        self.collection = mongo.get_collection_db_pacientes()
    
    @token_required
    def get(self, request, id):
        """
        Obtener un paciente específico por ID.
        
        Parámetros:
            id: ObjectId de MongoDB del paciente
        """
        try:
            item = self.collection.find_one({"_id": ObjectId(id)})
            if item:
                item['_id'] = str(item['_id'])
                return Response(item)
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(exclude=True)
    @token_required
    def put(self, request, id):
        """
        Actualizar un registro de paciente.
        
        Parámetros:
            id: ObjectId de MongoDB del paciente
        """
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
    
    @extend_schema(exclude=True)
    @token_required
    def delete(self, request, id):
        """
        Eliminar un registro de paciente.
        
        Parámetros:
            id: ObjectId de MongoDB del paciente
        """
        try:
            result = self.collection.delete_one({"_id": ObjectId(id)})
            if result.deleted_count:
                return Response({"message": "Eliminado correctamente"})
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)