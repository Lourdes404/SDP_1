from django.contrib import admin
from django.urls import path
from proyecto.views import index  # Asegúrate de importar la vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', index, name='home'),  # URL para la vista
]