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

def get_db_petri():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Clinicbot-Petri"]
    collection = db["placas_petri"] 
    return collection

def get_db_users():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Clinicbot-Usuarios"]
    collection = db["usuarios"] 
    return collection

def get_db_tokens():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Clinicbot-Usuarios"]
    collection = db["api_tokens"] 
    return collection

def get_db_Logs_Access():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Clinicbot-Logs"]
    collection = db["Access"] 
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