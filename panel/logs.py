from datetime import datetime
from bson import ObjectId
from db_connection import get_db_Logs_Access

db_logs_access = get_db_Logs_Access();

def log_action(request, action, status, description=""):
    nuevo_log = {
        "timestamp": datetime.now(),
        "user_id": ObjectId(request.user.get('idUsuario')) if request.user and request.user.get('idUsuario') else None,
        "username_at_log": request.user.get('username') if request.user and request.user.get('username') else None,
        "ip_address": request.META.get('REMOTE_ADDR'),
        "action": action,
        "status": status,
        "description": description,
        "user_agent": request.META.get('HTTP_USER_AGENT', ''),
        #"request_path": "/api/login",
        #"request_method": "POST"
    }

    db_logs_access.insert_one(nuevo_log)

'''
{
    "_id": ObjectId("..."),
    "timestamp": ISODate("2024-05-22T15:30:10.123Z"),
    "user_id": ObjectId("60a7e..."),
    "username_at_log": "admin",
    "ip_address": "203.0.113.42",
    "action": "LOGIN",
    "status": "FAILURE",
    "description": "Invalid password provided.",
    "user_agent": "Mozilla/5.0 ...",
    "request_path": "/api/login",
    "request_method": "POST"
}


'''


'''

nueva_muestra = {
                "paciente_id": ObjectId(paciente_id),
                "identificacion": identificacion,
                "color": color,
                "posicion": posicion,
                #"fecha": fecha,
                "fecha": datetime.now().strftime("%Y-%m-%dT%H:%M")
            }
            db_muestras.insert_one(nueva_muestra)


'''