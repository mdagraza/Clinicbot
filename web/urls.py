# miapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('datos_pacientes/', datos_pacientes, name='datos_pacientes'),
    path('', home, name='home'),
    path('borrar_paciente/', borrar_paciente, name='borrar_paciente'),
    #path('muestras/', editar_muestra, name='editar_muestra'),
    path('borrar_muestra/', borrar_muestra, name='borrar_muestra'),
    path('obtener_muestras/<str:identificacion_paciente>/', obtener_muestras, name='obtener_muestras'),
    path('obtener_muestras_no_relacionadas/', obtener_muestras_no_relacionadas, name='obtener_muestras_no_relacionadas'),
    path('petri/', editar_petri, name='editar_petri'),
    path('borrar_petri/', borrar_petri, name='borrar_petri'),
    path('obtener_petri/<str:identificacion_paciente>/', obtener_petri, name='obtener_petri'),
    path('obtener_petri_no_relacionadas/', obtener_petri_no_relacionadas, name='obtener_petri_no_relacionadas'),
]
