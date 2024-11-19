from django.db import models
from django.contrib.auth.models import User

""" 
Tabla: rol de usuario
Asociación: User
Uso: Determinación de tipo de usuario, como estudiante y profesor
 """
class rolUsuario(models.Model):
    codigo_rol = models.IntegerField(null=False)
    codigo_rol_descripcion = models.CharField(null=False, max_length=20)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)


