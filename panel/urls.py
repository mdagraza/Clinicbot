from django.urls import path
from .views import registro, login_view, dashboard, logout_view, cambiar_contrasena

urlpatterns = [
    path('registro/', registro, name='registro'),
    path('login/', login_view, name='login'),
    path('', login_view),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('cambiar-contrasena/', cambiar_contrasena, name='cambiar_contrasena'),
]