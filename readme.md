# ClinicBot - Laboratorio Clinico Robotizado

ClinicBot es una plataforma avanzada de gestion y asistencia virtual diseñada para coordinar la operativa de un laboratorio clinico automatizado. El sistema integra robotica colaborativa, vision artificial y bases de datos seguras para la gestion y analisis de muestras biologicas (sangre y placas petri).

Este proyecto ha sido beneficiario de las ayudas del **Plan de Recuperacion, Transformacion y Resiliencia** financiado por los fondos europeos **Next Generation EU**, en una colaboracion estrategica entre el I.E.S. Saenz de Buruaga, CPR FP Montecastelo, Institut Escola municipal del Treball, Coveless Ingenieria y Universal Robots.

## Caracteristicas Principales

- **Automatizacion Clinica:** Recepcion y gestion de informacion de laboratorio robotizado.
- **Robotica Colaborativa:** Integracion con brazos roboticos para la manipulacion de muestras.
- **Vision Artificial:** Analisis inteligente de placas petri y clasificacion de muestras.
- **Arquitectura Industria 4.0:** Backend robusto desarrollado en Django para la monitorizacion en tiempo real.
- **Interfaz Intuitiva:** Panel de control diseñado para facilitar la interaccion entre el personal sanitario y los sistemas mecatronicos.

## Tecnologias Utilizadas

- **Lenguaje:** Python 3.10+
- **Framework Web:** Django (arquitectura MVC/MVT).
- **Base de Datos:** MongoDB (almacenamiento NoSQL seguro).
- **Contenedores:** Docker para el despliegue del servidor de base de datos.
- **Robotica:** Protocolos de comunicacion con Universal Robots.

## Requisitos del Sistema

- Python 3.10 o superior.
- Docker instalado y configurado.
- Base de datos MongoDB activa en el puerto 27017.

## Instalacion y Configuracion

### 1. Clonar el repositorio

```bash
git clone [https://github.com/mdagraza/Clinicbot.git](https://github.com/mdagraza/Clinicbot.git)
cd Clinicbot
```

### 2. Despliegue de la Base de Datos

```bash
docker run -d -p 27017:27017 --name mongo-server mongo
```

### 3. Configuracion del Entorno Virtual

```bash
# Crear entorno virtual
python -m venv ../entorno_virtual

# Activar en Linux/macOS
source ../entorno_virtual/bin/activate

# Activar en Windows
..\entorno_virtual\Scripts\activate
```

### 4. Instalacion de dependencias

```bash
pip install -r requirements.txt
```

### Ejecución

```bash
python manage.py runserver 0.0.0.0:80
```
