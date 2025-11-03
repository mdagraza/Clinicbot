from pymongo import MongoClient
from threading import Lock

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_NAME1 = 'Clinicbot-Pacientes'
MONGODB_NAME2 = 'Clinicbot-Muestras'
MONGODB_NAME3 = 'Clinicbot-Petri'

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
    
class MongoDBConnection_Petri:
    def __init__(self):
        self.client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        self.db = self.client[MONGODB_NAME3]
        
    def get_collection(self, collection_name):
        return self.db[collection_name]
    
class MongoDBConnection_Usuarios:
    def __init__(self):
        self.client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        self.db = self.client['Clinicbot-Usuarios']
        
    def get_collection(self, collection_name):
        return self.db[collection_name]

class MongoDBConnection:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        return cls._instance
    
    def get_collection_db_muestras(self, collection: str = "muestras"): #Se pone por defecto la colección que mas se usa, si se necesita otra, se define en la llamada
        self.db = self.client["Clinicbot-Muestras"]
        return self.db[collection]
    
    def get_collection_db_petri(self, collection: str = "petri"):
        self.db = self.client["Clinicbot-Petri"]
        return self.db[collection]
    
    def get_collection_db_pacientes(self, collection: str = "pacientes"):
        self.db = self.client["Clinicbot-Pacientes"]
        return self.db[collection]
    
    def get_collection_db_log(self, collection: str = "access"):
        self.db = self.client["Clinicbot-Logs"]
        return self.db[collection]
    
    def get_collection_db_usuarios(self, collection: str = "usuarios"):
        self.db = self.client["Clinicbot-Usuarios"]
        return self.db[collection]
    
    def get_collection_db(self, db: str, collection: str):
        self.db = self.client[db]
        return self.db[collection]