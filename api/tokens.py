from db_connection import MongoDBConnection_Usuarios
from datetime import datetime, timedelta
import secrets
from bson import ObjectId

class TokenManager:
    def __init__(self):
        self.mongodb = MongoDBConnection_Usuarios() 
        self.collection = self.mongodb.get_collection('api_tokens')
    
    def generate_token(self, user_id, expires_in_hours=24):
        # Generar un token aleatorio seguro
        token = secrets.token_hex(32)

        # Verificar que el token no exista en la base de datos
        while self.collection.find_one({"token": token}):
            token = secrets.token_hex(32)
        
        # Calcular fecha de expiración
        expires_at = datetime.now() + timedelta(days=expires_in_hours/24)
        
        # Almacenar en MongoDB
        token_data = {
            "user_id": ObjectId(user_id),
            "token": token,
            "created_at": datetime.now(),
            "expires_at": expires_at,
            "is_active": True
        }
        
        self.collection.insert_one(token_data)
        return token
    
    def validate_token(self, token):
        # Buscar el token en la base de datos
        token_data = self.collection.find_one({
            "token": token,
            "is_active": True,
            "expires_at": {"$gt": datetime.now()}
        })
        
        return token_data
    
    def revoke_token(self, token):
        self.collection.update_one(
            {"token": token},
            {"$set": {"is_active": False}}
        )