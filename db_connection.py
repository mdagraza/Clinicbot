from pymongo import MongoClient

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_NAME1 = 'Clinicbot-Pacientes'
MONGODB_NAME2 = 'Clinicbot-Muestras'

def get_db_pacientes():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Clinicbot-Pacientes"]
    collection = db["pacientes"] 
    return collection

def get_db_muestras():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Clinicbot-Muestras"]
    collection = db["muestras"] 
    return collection

class MongoDBConnection_Pacientes:
    def __init__(self):
        self.client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        self.db = self.client[MONGODB_NAME1]
        
    def get_collection(self, collection_name):
        return self.db[collection_name]
    
class MongoDBConnection_Muestras:
    def __init__(self):
        self.client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        self.db = self.client[MONGODB_NAME2]
        
    def get_collection(self, collection_name):
        return self.db[collection_name]
    
class MongoDBConnection_Usuarios:
    def __init__(self):
        self.client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        self.db = self.client['Clinicbot-Usuarios']
        
    def get_collection(self, collection_name):
        return self.db[collection_name]