"""
URL configuration for Clinicbot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny

urlpatterns = [
    #path('admin/', admin.site.urls),
    
    # Swagger/OpenAPI documentation
    #path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    #path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("api/schema/", SpectacularAPIView.as_view(authentication_classes=[], permission_classes=[AllowAny]), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema", authentication_classes=[], permission_classes=[AllowAny]), name="swagger-ui"),
    
    path('', include('web.urls')),   
    path('panel/', include('panel.urls')), 
    path('api/', include('api.urls')),   
    path('panel-u/', include('panel_admin.urls')),   
]

#Para mostrar las imagenes de MEDIA en modo DEBUG
# Esto es necesario para que Django sirva archivos estáticos y de medios durante el desarrollo.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''path('', views.hello), #'' Es la pagin principal, y luego lo que debe cargar
    path('', include('projects.urls')), #Traer al principal, las urls creadas en la app
    path('persona/', views.persona),
    path('persona/<int:id>/', views.prueba),
    path('', include('persona.urls')),
    path('form/', views.form),'''