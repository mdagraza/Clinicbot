from pymongo import MongoClient
from threading import Lock

#Estos datos deberían moverse fuera de aquí para no estar en git
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

    
class MongoDBConnection:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                #TODO: Para poner user y pass           
                    #cls._instance.client = MongoClient(
                    #    host=MONGODB_HOST,
                    #    port=MONGODB_PORT,
                    #    username=MONGODB_USER,
                    #    password=MONGODB_PASS,
                    #    authSource="admin"
                    #)
                cls._instance.client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        return cls._instance
    
    def get_collection_db_muestras(self, collection: str = "muestras"): #Se pone por defecto la colección que mas se usa, si se necesita otra, se define en la llamada
        self.db = self.client["Clinicbot-Muestras"]
        return self.db[collection]
    
    def get_collection_db_petri(self, collection: str = "placas_petri"):
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