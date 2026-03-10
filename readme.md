# Clinicbot

Clinicbot es un asistente virtual diseñado para recibir y gestionar la información de un laboratorio clínico robotizado.

## Características

- Gestión de muestras de sangre y análisis de placas petri.
- Interfaz intuitiva y fácil de usar.

## Requisitos

- Python 3.10+
- Librerías detalladas en `requirements.txt`
- Base de datos MongoDB

## Instalación

```bash
git clone https://gitlab.com/mdagraza/clinicbot.git # gitlab

#Crear entorno virtual, en paralelo a la carpeta del proyecto Clinicbot
python -m venv entorno_virtual

#Linux
source entorno_virtual/bin/activate
#Windows
entorno_virtual\Scripts\activate

#Instalar paquetes desde el archivo requirements.txt
pip install -r requirements.txt
```

Entorno_Virtual > Clinicbot

## Activar servidor

```bash
#Activar servidor
(entorno_virtual)Clinicbot$ python manage.py runserver 0.0.0.0:80

#Crear datos de prueba
(entorno_virtual)Clinicbot$ python manage.py seed_data <username>
```

## Licencia

Este proyecto está bajo la licencia MIT.
