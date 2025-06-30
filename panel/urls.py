from django.urls import path
from .views import *

urlpatterns = [
    path('registro/', registro, name='registro'),
    path('editar_usuario', editar_usuario, name='editar_usuario'),
    path('activacion_usuario', activacion_usuario, name='activacion_usuario'),
    path('borrar_usuario', borrar_usuario, name='borrar_usuario'),
    path('login/', login_view, name='login'),
    path('', login_view),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
]