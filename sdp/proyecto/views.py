from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages

""" import os
import subprocess

import msal
import requests

from sklearn.feature_extraction.text import TfidfVectorizer """


def index(request):
    return render(request,'index.html')

def iniciarSesion(request):
    return render(request,'iniciarSesion.html')

############################################################################################################################
"""
Vista: Registrarse
Función: crear usuarios
"""
def registrarse(request):
    if request.method == 'POST':
        # Capturamos los datos del formulario
        rol = request.POST.get('rol')
        nombre1 = request.POST.get('nombre1')
        nombre2 = request.POST.get('nombre2')
        apellido1 = request.POST.get('apellido1')
        apellido2 = request.POST.get('apellido2')
        correo = request.POST.get('correo')
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contrasena')
        confirmar_contraseña = request.POST.get('confirmar_contrasena')
        print('Information was received!')
        # Validaciones simples
        if not rol or not nombre1 or not apellido1 or not correo or not usuario or not contraseña or not confirmar_contraseña:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)
        
        if contraseña != confirmar_contraseña:
            return JsonResponse({'error': 'Las contraseñas no coinciden'}, status=400)

        if User.objects.filter(username=usuario).exists():
            return JsonResponse({'error': 'El nombre de usuario ya existe'}, status=400)

        # Crear el usuario
        try:
            user = User.objects.create_user(username=usuario, email=correo, password=contraseña)
            user.first_name = nombre1
            user.last_name = apellido1
            user.save()
            print("Able to create user!")

            # Iniciar sesión automáticamente
            login(request, user)

            return JsonResponse({'success': 'Usuario creado exitosamente, redirigiendo a la página de inicio de sesión'})
        except Exception as e:
            print("Unable to create user!")
            return JsonResponse({'error': f'Error al crear el usuario: {str(e)}'}, status=500)
    return render(request,'registrarse.html')
############################################################################################################################



def inicio(request):
    return render(request,'inicio.html')

def adjuntar(request):
    return render(request,'adjuntar.html')


"""
Templates: PÁGINAS DE ERROR
Descripción: Comunes errores que puede obtener el usuario.
"""
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)

def custom_403_view(request, exception):
    return render(request, '403.html', status=403)

def custom_400_view(request, exception):
    return render(request, '400.html', status=400)