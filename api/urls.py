from django.urls import path
from .views import *

urlpatterns = [
    path('pacientes/', ItemListView_Pacientes.as_view(), name='pacientes-list'),
    path('pacientes/<str:id>/', ItemDetailView_Pacientes.as_view(), name='pacientes-detail'),
    path('pacientes/<str:id>/muestras/', ItemListView_MuestrasPorPaciente.as_view(), name='paciente-muestras-list'),
    path('muestras/', ItemListView_Muestras.as_view(), name='muestras-list'),
    path('muestras/<str:id>/', ItemDetailView_Muestras.as_view(), name='muestras-detail'),

    path('token/', TokenView.as_view(), name='token'),

    path('imagen/', Save_Images.as_view(), name='save_images'),
]
