from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView
from django.views.static import serve
from proyecto.views import reporte,ListadoEstudiantes,detalleForm,buscar,ver,index,iniciarSesion,registrarse, inicio, adjuntar # Asegúrate de importar la vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'), 
    path('iniciarSesion/',iniciarSesion, name='iniciarSesion'),
    path('registrarse/',registrarse, name='registrarse'),
    path('inicio/',inicio, name='inicio'),
    path('adjuntar/',adjuntar, name='adjuntar'),
    path('verTesis/',ver,name='ver'),
    path('buscar/',buscar,name='buscar'),
    path('detalle/', detalleForm, name='detalleForm'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('listadoEstudiantes/',ListadoEstudiantes,name='listadoEstudiantes'),
    path('reporteAnalisis/', reporte, name='reporte')


]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
# Configuración de los handlers para errores
handler404 = 'proyecto.views.custom_404_view'  
handler500 = 'proyecto.views.custom_500_view'  
handler403 = 'proyecto.views.custom_403_view'  
handler400 = 'proyecto.views.custom_400_view'  