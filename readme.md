# Clinicbot

Clinicbot es un asistente virtual diseñado para recibir y gestionar la información de un laboratorio clínico robotizado.

## Características

- Gestión de muestras de sangre y análisis de placas petri.
- Interfaz intuitiva y fácil de usar.

## Requisitos

- Python 3.10+
- Librerías detalladas en `requirements.txt`
- Base de datos MongoDB : Instalación sobre un mongo-server en docker en el puerto 27017

## Instalación

```bash
git clone https://github.com/mdagraza/Clinicbot.git # En caso de github
git clone https://gitlab.com/mdagraza/clinicbot.git # En caso de gitlab

#Crear entorno virtual, en paralelo a la carpeta del proyecto Clinicbot
python -m venv entorno_virtual

#Linux
source entorno_virtual/bin/activate
```

```powershell
#Windows
entorno_virtual\Scripts\activate
```

```bash
#Archivo dentro de la carpeta de Clinicbot
pip install -r requirements.txt
```

Entorno_Virtual > Clinicbot

## Activar servidor

```bash
(entorno_virtual)Clinicbot$ python manage.py runserver
```

## Licencia

Este proyecto está bajo la licencia MIT.
