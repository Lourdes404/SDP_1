from django.db import models
from django.contrib.auth.models import User

""" 
METODO UTILIZADO PARA SUBIR DOCUMENTOS
Asociación: Documento
Uso: Determinación del nombre de una carpeta según el nombre de usuario
Crea un nombre único para la carpeta basado en el username del usuario
El archivo se guardará en: MEDIA_ROOT/Documentos/<username>/<filename>
 """
def user_directory_path(instance, filename):
    return f'Documentos/{instance.usuario.username}/{filename}'

""" 
Tabla: rol de usuario
Asociación: User
Uso: Determinación de tipo de usuario, como estudiante y profesor
 """
class rolUsuario(models.Model):
    codigo_rol = models.IntegerField(null=False)
    codigo_rol_descripcion = models.CharField(null=False, max_length=20)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)


""" 
Tabla: documentos de tesis
Asociación: User
Uso: Asociar un documento pdf con el user
 """
class documento(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    ubicacion = models.FileField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return f"Documento de {self.usuario.username}"


""" 
Tabla: informacion de proyecto de tesis
Asociación: documento
Uso: tener los detalles de los documentos subidos
 """
class InformacionAnalizada(models.Model):
    documento = models.OneToOneField(documento, on_delete=models.CASCADE)
    nombre = models.TextField(blank=True, null=True)
    pregunta = models.TextField(blank=True, null=True)
    objetivo = models.TextField(blank=True, null=True)
    hipotesis = models.TextField(blank=True, null=True)
    justificacion = models.TextField(blank=True, null=True)
    problema = models.TextField(blank=True, null=True)

""" 
Tabla: Analisis de similitud
Asociación: InformacionAnalizada
Uso: Analizar la info de tesis, que se asocia al doc, que a su vez se asocia al user
 """
class AnalisisSimilitud(models.Model):
    informacion_analizada = models.ForeignKey(InformacionAnalizada,on_delete=models.CASCADE)
    fecha_analisis = models.DateTimeField(auto_now_add=True)
    porcentaje_similitud = models.DecimalField(max_digits=5, decimal_places=2)

