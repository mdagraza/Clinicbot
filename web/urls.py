# miapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('datos_pacientes/', datos_pacientes, name='datos_pacientes'),
    path('', home, name='home'),
    path('borrar_paciente/', borrar_paciente, name='borrar_paciente'),
    path('muestras/', editar_muestra, name='editar_muestra'),
    path('borrar_muestra/', borrar_muestra, name='borrar_muestra'),
    path('obtener_muestras/<str:identificador_paciente>/', obtener_muestras, name='obtener_muestras'),
    path('petri/', editar_petri, name='editar_petri'),
    path('borrar_petri/', borrar_petri, name='borrar_petri'),
    path('obtener_petri/<str:identificador_paciente>/', obtener_petri, name='obtener_petri'),
]
