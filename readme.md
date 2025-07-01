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
git clone https://github.com/tu_usuario/Clinicbot.git # En caso de github
git clone https://gitlab.com/tu_usuario/clinicbot.git # En caso de gitlab
cd Clinicbot
python -m venv entorno_virtual
source entorno_virtual/bin/activate  # En Windows: entorno_virtual\Scripts\activate
pip install -r requirements.txt
```

Entorno_Virtual > Clinicbot

## Activar servidor
```bash
(entorno_virtual)Clinicbot$ python manage.py runserver
```

## Uso

```bash
python main.py
```

## Licencia

Este proyecto está bajo la licencia MIT.