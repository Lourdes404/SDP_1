from django.contrib import admin
from django.urls import path
from proyecto.views import index,iniciarSesion,registrarse, inicio, adjuntar # Asegúrate de importar la vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'), 
    path('iniciarSesion/',iniciarSesion, name='iniciarSesion'),
    path('registrarse/',registrarse, name='registrarse'),
    path('inicio/',inicio, name='inicio'),
    path('adjuntar/',adjuntar, name='adjuntar')
]