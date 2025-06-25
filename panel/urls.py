from django.urls import path
from .views import *

urlpatterns = [
    path('registro/', registro, name='registro'),
    path('login/', login_view, name='login'),
    path('', login_view),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
]