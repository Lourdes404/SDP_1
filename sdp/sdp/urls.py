from django.contrib import admin
from django.urls import path
from proyecto.views import buscar,ver,index,iniciarSesion,registrarse, inicio, adjuntar # Asegúrate de importar la vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'), 
    path('iniciarSesion/',iniciarSesion, name='iniciarSesion'),
    path('registrarse/',registrarse, name='registrarse'),
    path('inicio/',inicio, name='inicio'),
    path('adjuntar/',adjuntar, name='adjuntar'),
    path('verTesis/',ver,name='ver'),
    path('buscar/',buscar,name='buscar')
]


# Configuración de los handlers para errores
handler404 = 'proyecto.views.custom_404_view'  
handler500 = 'proyecto.views.custom_500_view'  
handler403 = 'proyecto.views.custom_403_view'  
handler400 = 'proyecto.views.custom_400_view'  