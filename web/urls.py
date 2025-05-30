# miapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('editar/', editar_usuario, name='editar_usuario'),
    path('', home2, name='home2'),
    path('borrar_usuario/', borrar_usuario, name='borrar_usuario'),
    path('muestras/', editar_muestra, name='editar_muestra'),
    path('borrar_muestra/', borrar_muestra, name='borrar_muestra'),
    path('obtener_muestras/<str:usuario_id>/', obtener_muestras, name='obtener_muestras'),
]
