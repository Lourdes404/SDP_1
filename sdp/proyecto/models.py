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
    


