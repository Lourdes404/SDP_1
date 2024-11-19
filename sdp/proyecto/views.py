from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from .models import rolUsuario
from django.contrib.auth.decorators import login_required
from datetime import datetime

""" import os
import subprocess

import msal
import requests

from sklearn.feature_extraction.text import TfidfVectorizer """

############################################################################################################################
"""
Vista: Página principal del sitio
Función: loguear al usuario, crear usuarios y hacer búsquedas
"""
def index(request):
    return render(request,'index.html')
############################################################################################################################


############################################################################################################################
"""
Vista: Iniciar sesión
Función: loguear al usuario
"""
def iniciarSesion(request):
    if request.method == "POST":
        # Capturar los datos del formulario
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contrasena')
        print('Information has been received!')
        # Intentar autenticar al usuario
        user = authenticate(request, username=usuario, password=contraseña)

        if user is not None:
            login(request, user)
            return redirect('/inicio/') 
        else:
            print("You can't sign in!")
            error_message = "Usuario o contraseña incorrectos."
            return render(request, 'iniciarSesion.html', {'error_message': error_message})

    # Si es una solicitud GET, solo mostrar la plantilla
    return render(request, 'iniciarSesion.html')
############################################################################################################################

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
        
        codigo_rolp = 0
        if rol == 'estudiante':
            rol = 'Estudiante'
            codigo_rolp = 1
            print("Rol has been received as student!")
        if (rol == 'profesor'):
            rol = 'Profesor'
            codigo_rolp = 2
            print("Rol has been received as proffessor!")


        # Crear el usuario
        try:
            user = User.objects.create_user(username=usuario, email=correo, password=contraseña)
            user.first_name = nombre1
            user.last_name = apellido1
            user.save()

            print("Able to create user!")
            rol = rolUsuario.objects.create(codigo_rol=codigo_rolp,codigo_rol_descripcion=rol,usuario=user)
            print("The rol has been inserted and linked to the user!")
            # Iniciar sesión automáticamente
            login(request, user)

            return JsonResponse({'success': 'Usuario creado exitosamente, redirigiendo a la página de inicio de sesión'})
        except Exception as e:
            print("Unable to create user!")
            return JsonResponse({'error': f'Error al crear el usuario: {str(e)}'}, status=500)
    return render(request,'registrarse.html')
############################################################################################################################

############################################################################################################################
"""
Vista: INICIO
Función: crear acceso a todas las opciones del usuario
"""
def inicio(request):
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
        email = request.user.email
        print(email)
        nombre_completo = f"{request.user.first_name} {request.user.last_name}"
        nombre1 = request.user.first_name
    
        # Obtener el rol del usuario desde la tabla `rolUsuario`
        try:
            rol = rolUsuario.objects.get(usuario=request.user)
        except rolUsuario.DoesNotExist:
            # Si no tiene un rol asociado, lanzar error 403
            return render(request, '403.html', status=403)

        # Validar que el rol tiene acceso (usuarios tipo 1 y 2)
        if rol.codigo_rol not in [1, 2]:  # Solo estudiantes (1) y profesores (2) tienen acceso
            return render(request, '403.html', status=403)
        
        print(f"Usuario: {username}, Rol: {rol.codigo_rol_descripcion}")  # Debug

    else:
        # Usuario no autenticado
        return render(request, '401.html', status=401)

    #saludo para decir buenos días, buenas tardes o buenas noches
    hora_actual = datetime.now().hour
    if 5 <= hora_actual < 12:
        saludo = "Buenos días"
    elif 12 <= hora_actual < 18:
        saludo = "Buenas tardes"
    else:
        saludo = "Buenas noches"


    # Pasar los datos al contexto
    context = {
        'username': username,
        'email': email,
        'nombre_completo': nombre_completo,
        'saludo': saludo,
        'nombre1': nombre1,
        'rol': rol.codigo_rol_descripcion,
    }
    return render(request,'inicio.html',context)
############################################################################################################################


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