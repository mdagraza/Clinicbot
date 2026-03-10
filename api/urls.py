from django.urls import path
from api.views.pacientes import *
from api.views.muestras import *
from api.views.petri import *
from api.views.token import *
from api.views.imagen import *

urlpatterns = [
    path('pacientes/', ItemListView_Pacientes.as_view(), name='pacientes-list'),
    path('pacientes/<str:id>/', ItemDetailView_Pacientes.as_view(), name='pacientes-detail'),
    path('muestras/', ItemListView_Muestras.as_view(), name='muestras-list'),
    path('muestras-no-asociadas/', ItemListView_MuestrasNoAsociadas.as_view(), name='muestras-no-asociadas-list'),
    path('muestras/<str:id>/', ItemDetailView_Muestras.as_view(), name='muestras-detail'),
    path('petri/', ItemListView_Petri.as_view(), name='petri-list'),
    path('petri/<str:id>/', ItemDetailView_Petri.as_view(), name='petri-detail'),
    path('petri-no-asociadas/', ItemListView_PetriNoAsociadas.as_view(), name='petri-no-asociadas-list'),

    path('token/', TokenView.as_view(), name='token'),

    path('imagen/', Save_Images.as_view(), name='save_images'),
]