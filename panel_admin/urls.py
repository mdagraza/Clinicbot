from django.urls import path
from .views import *

urlpatterns = [
    path('', panel_datos, name='panel_datos'),
    path('tokens', panel_tokens, name='panel_tokens'),
    path('usuarios', panel_usuarios, name='panel_usuarios'),
    path('cambiar_contrasena', cambiar_contrasena, name='cambiar_contrasena'),
]