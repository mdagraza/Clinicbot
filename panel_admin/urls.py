from django.urls import path
from .views import general

urlpatterns = [
    path('general/', general, name='general'),

]