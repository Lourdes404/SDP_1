import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from .models import rolUsuario, documento, InformacionAnalizada,AnalisisSimilitud
from django.contrib.auth.decorators import login_required
from datetime import datetime
import time
from django.core.files.storage import FileSystemStorage
import openai
import os
from PyPDF2 import PdfReader
from django.conf import settings

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.core.exceptions import ValidationError

PENAI_API_KEY = ""

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
############################################################################################################################
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

"""
Vista: adjuntar tesis
Función: subir el pdf para la tesis
"""
############################################################################################################################
def adjuntar(request):
    modal_visible = False  # Indicador para mostrar el modal
    file_url = None
    documento_existente = None  # Para verificar si el usuario ya tiene un documento

    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        nombre_completo = f"{request.user.first_name} {request.user.last_name}"
        nombre1 = request.user.first_name
    
        # Obtener el rol del usuario desde la tabla `rolUsuario`
        try:
            rol = rolUsuario.objects.get(usuario=request.user)
        except rolUsuario.DoesNotExist:
            # Si no tiene un rol asociado, lanzar error 403
            return render(request, '403.html', status=403)

        """ # Validar que el rol tiene acceso (usuarios tipo 1 y 2)
        if rol.codigo_rol != 1:  # Solo estudiantes (1) y profesores (2) tienen acceso
            return render(request, '403.html', status=403) """
        
        print(f"Usuario: {username}, Rol: {rol.codigo_rol_descripcion}")  # Debug
        
        # Verificar si el usuario ya tiene un documento
        try:
            documento_existente = documento.objects.get(usuario=request.user)
            file_url = documento_existente.ubicacion.url  # Obtener la URL del documento actual
            print(f"Documento existente encontrado: {file_url}")  # Debug
        except documento.DoesNotExist:
            print("No hay documento existente para este usuario.")  # Debug

        if request.method == 'POST':
            uploaded_file = request.FILES.get('documento')  # Obtener el archivo del formulario
            print(f"Archivo recibido: {uploaded_file}")  # Depuración
            
            if uploaded_file and uploaded_file.name.endswith('.pdf'):
                if documento_existente:
                    print(documento_existente)
                    # Mostrar un modal para confirmar la actualización
                    if 'confirmar_actualizacion' in request.POST:
                        # El usuario confirmó la actualización
                        documento_existente.ubicacion = uploaded_file
                        documento_existente.save()
                        file_url = documento_existente.ubicacion.url
                        print(f"Documento actualizado en: {file_url}")  # Debug
                        modal_visible = True
                    else:
                        # El usuario aún no confirmó, mostrar el modal
                        modal_visible = 'actualizacion'
                else:
                    # Crear un nuevo documento para el usuario
                    nuevo_documento = documento(usuario=request.user, ubicacion=uploaded_file)
                    nuevo_documento.save()
                    file_url = nuevo_documento.ubicacion.url
                    print(f"Nuevo documento guardado en: {file_url}")  # Debug
                    modal_visible = True
            else:
                # Si el archivo no es PDF
                print("Error: El archivo no es PDF")
                modal_visible = False
                file_url = None
        else:
            modal_visible = False
    else:
        # Usuario no autenticado
        return render(request, '401.html', status=401)
    
    # Pasar los datos al contexto
    context = {
        'username': username,
        'email': email,
        'nombre_completo': nombre_completo,
        'nombre1': nombre1,
        'apellido1': request.user.last_name,
        'rol': rol.codigo_rol_descripcion,
        'modal_visible': modal_visible,
        'file_url': file_url,
        'documento_existente': documento_existente,
    }
    
    return render(request, 'adjuntar.html', context)
############################################################################################################################

"""
Vista: ver detalle de la tesis tesis
Función: ver los detalles de la tesis
"""
############################################################################################################################
def ver(request):
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
        if rol.codigo_rol != 1:  # Solo estudiantes (1) y profesores (2) tienen acceso
            return render(request, '403.html', status=403)
        
        print(f"Usuario: {username}, Rol: {rol.codigo_rol_descripcion}")  # Debug
        ##################################################################################
        #PROCEDIMIENTO DE LA VISTA
        documentos  = documento.objects.filter(usuario=request.user)
        doc = documentos.first()
        tesisLista = InformacionAnalizada.objects.filter(documento = doc)
        tesis = tesisLista.first()
        ruta_relativa = doc.ubicacion.name  # Esto debería ser "Documentos/lourdes2/Proyecto_3.pdf"
        ruta_completa = f"{settings.MEDIA_URL}{ruta_relativa}"  # "media/Documentos/lourdes2/Proyecto_3.pdf"
        print(ruta_completa)
    else:
        # Usuario no autenticado
        return render(request, '401.html', status=401)
    
    # Pasar los datos al contexto
    context = {
        'username': username,
        'email': email,
        'nombre_completo': nombre_completo,
        'nombre1': nombre1,
        'rol': rol.codigo_rol_descripcion,
        'nombreT': tesis.nombre,
        'pregunta': tesis.pregunta,
        'objetivo': tesis.objetivo,
        'hipotesis': tesis.hipotesis,
        'justificacion': tesis.justificacion,
        'problema': tesis.problema,
        'path': ruta_completa,
        'nombredoc': os.path.basename(ruta_relativa)
    }
    return render(request,'ver_tesis_detalle.html',context)
############################################################################################################################


"""
Vista: buscar anteproyectos de tesis 
Función: buscar detalles de la tesis
"""
############################################################################################################################
def buscar(request):
    # Verificar si el usuario está autenticado
    if not request.user.is_authenticated:
        return render(request, '403.html', status=403)

    # Obtener el rol del usuario desde la tabla `rolUsuario`
    try:
        rol = rolUsuario.objects.get(usuario=request.user)
    except rolUsuario.DoesNotExist:
        return render(request, '403.html', status=403)

    if rol.codigo_rol != 1:  # Verificar permisos de rol
        return render(request, '403.html', status=403)

    # Inicializar el contexto
    resultados = []
    query = request.GET.get('q', '').strip()  # Obtener el texto de búsqueda del usuario
    print(query)
    if query:  # Si hay un texto para buscar
        # Obtener todas las entradas de `InformacionAnalizada`
        documentos = InformacionAnalizada.objects.all()

        # Concatenar los campos de cada documento en una sola cadena de texto
        corpus = []
        ids = []
        for doc in documentos:
            texto_completo = f"{doc.nombre or ''} {doc.pregunta or ''} {doc.objetivo or ''} {doc.hipotesis or ''} {doc.justificacion or ''} {doc.problema or ''}"
            corpus.append(texto_completo)
            ids.append(doc.id)  # Guardar ID para referencia posterior
            print(texto_completo)
            print(ids)
        # Crear un vector TF-IDF para medir similitudes
        print('Crear un vector TF-IDF para medir similitudes')
        vectorizer = TfidfVectorizer().fit_transform([query] + corpus)  # El primer elemento será el texto de búsqueda
        print(vectorizer)
        cosine_similarities = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()  # Calcular similitud de coseno
        print(cosine_similarities)
        print('Ordenar los documentos por similitud (de mayor a menor)')
        documentos_similares = sorted(
            zip(ids, cosine_similarities),
            key=lambda x: x[1],
            reverse=True
        )
        print(documentos_similares)

        print('Filtrar documentos con similitud mayor a 0')
        for doc_id, similarity in documentos_similares:
            if similarity > 0:
                doc = InformacionAnalizada.objects.get(id=doc_id)
                resultados.append({
                    'nombre': doc.nombre,
                    'autor': doc.documento.usuario.first_name if doc.documento.usuario else 'No disponible',
                    'similitud': round(similarity * 100, 2)  # Convertir a porcentaje
                })

    print('Contexto para renderizar la página')
    print(resultados)
    context = {
        'resultados': resultados,
        'query': query,
    }
    return render(request, 'buscarE.html', context)
############################################################################################################################

"""
Vista: Detalles analizados del proyecto 
Función: mostrar el analisis y si es necesario, editarlo
"""
############################################################################################################################
def detalleForm(request):
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
        
        print(f"Usuario: {username}, Rol: {rol.codigo_rol_descripcion}")  # Debug

    else:
        # Usuario no autenticado
        return render(request, '401.html', status=401)
    ##################################################################################
    #PROCEDIMIENTO DE LA VISTA
    if request.method == 'POST':
        nombreTesis = request.POST.get('nombre')
        preguntaT = request.POST.get('pregunta')
        objetivoT = request.POST.get('objetivo')
        hipotesisT = request.POST.get('hipotesis')
        justificacionT = request.POST.get('justificacion')
        problemaT = request.POST.get('problema')
        
        try:
            documentos  = documento.objects.filter(usuario=request.user)
            doc = documentos.first()
            if not doc:
                print('No se encontró ningún documento para este usuario')
                return
            tesis = InformacionAnalizada(
                documento = doc,
                nombre = nombreTesis,
                pregunta = preguntaT,
                objetivo = objetivoT,
                hipotesis = hipotesisT,
                justificacion = justificacionT,
                problema = problemaT
            )
            tesis.save()
            print('Se insertó correctamente')
            return redirect('inicio')
        except:
            print('Hubo un error al insertar en esta tabla')

    # Pasar los datos al contexto
    context = {
        'username': username,
        'email': email,
        'nombre_completo': nombre_completo,
        'nombre1': nombre1,
        'rol': rol.codigo_rol_descripcion,
    }
    return render(request,'proyectoForm.html',context)
############################################################################################################################

"""
Vista: Detalles analizados del proyecto 
Función: mostrar el analisis y si es necesario, editarlo
"""
############################################################################################################################
def ListadoEstudiantes(request):
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
        
        print(f"Usuario: {username}, Rol: {rol.codigo_rol_descripcion}")  # Debug

    else:
        # Usuario no autenticado
        return render(request, '401.html', status=401)
    
    # Pasar los datos al contexto
    context = {
        'username': username,
        'email': email,
        'nombre_completo': nombre_completo,
        'nombre1': nombre1,
        'rol': rol.codigo_rol_descripcion,
    }
    return render(request,'listadoEstudiantes.html',context)
############################################################################################################################

"""
Vista: Reporte de análisis
Función: mostrar el analisis de la tesis de studiante
"""
############################################################################################################################
def reporte(request):
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
        
        print(f"Usuario: {username}, Rol: {rol.codigo_rol_descripcion}")  # Debug
        print('Obtener info de la tesis para su análisis')
        documentos  = documento.objects.filter(usuario=request.user)
        doc = documentos.first()
        tesisLista = InformacionAnalizada.objects.filter(documento = doc)
        informacion = tesisLista.first()
        print(informacion.nombre)
        print('Validar máximo análisis')
        validar_maximo_analisis(informacion)
        print(validar_maximo_analisis)
        # Calcular porcentaje de similitud (ejemplo de lógica externa)
        porcentaje_similitud = calcular_similitud(informacion)
        print('Porcentaje de similitud...')
        print(porcentaje_similitud)
        # Crear análisis
        analisis = AnalisisSimilitud.objects.create(
            informacion_analizada=informacion,
            porcentaje_similitud=porcentaje_similitud
        )
        print('Analisis guardado con el porcentaje: ')
        print(analisis.porcentaje_similitud)
    else:
        # Usuario no autenticado
        return render(request, '401.html', status=401)
    
    # Pasar los datos al contexto
    context = {
        'username': username,
        'email': email,
        'nombre_completo': nombre_completo,
        'nombre1': nombre1,
        'rol': rol.codigo_rol_descripcion,
        'analisis': analisis,
    }
    return render(request,'reporte.html',context)
############################################################################################################################

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



"""
------------NO VISTAS---------------------
PROCEDIMIENTOS ÚTILES DEL PROYECTO

NO AGREGAR VISTAS ABAJO POR FAVOR
"""
def extract_text_from_pdf(url_path):
    # Construir la ruta de archivo desde la URL
    relative_path = url_path.replace(settings.MEDIA_URL, "")  # Eliminar la parte de '/media/'
    file_path = os.path.join(settings.MEDIA_ROOT, relative_path)  # Construir la ruta completa
    
    # Leer el archivo PDF
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    
    return text


def split_text_into_chunks(text, max_tokens=8192):
    # Función para dividir el texto en fragmentos de tamaño máximo de tokens permitido
    tokens = text.split()  # Suponiendo que cada palabra es un token
    chunks = []
    
    while len(tokens) > max_tokens:
        chunk = " ".join(tokens[:max_tokens])
        chunks.append(chunk)
        tokens = tokens[max_tokens:]
    if tokens:
        chunks.append(" ".join(tokens))
    
    return chunks

def analyze_with_openai(text):
    openai.api_key = PENAI_API_KEY
    chunks = split_text_into_chunks(text)
    print(datetime.timestamp.__str__)
    #while True:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Analiza la pregunta de tesis. Si no encuentras nada, porfis solo responde: None:"},
                {"role": "user", "content": text}
            ]
        )
        print(response['choices'][0]['message']['content'])


        return response['choices'][0]['message']['content']
    except openai.error.RateLimitError as e:
        # Esperar el tiempo que el mensaje de error indique antes de reintentar
        print(f"Rate limit reached. Waiting for 60 seconds...")
        time.sleep(60)  # Esperar antes de reintentar

def analizar_prueba():

    #Texto de prueba
    url_path = "/media/Documentos/lourdes2/Entrega4.pdf"
    text = extract_text_from_pdf(url_path)
    print(text)
    # Extraer texto y analizar con OpenAI
    analysis = analyze_with_openai(text)

    print(JsonResponse({"analysis": analysis}))


def validar_maximo_analisis(tesis):
    print('Cantidad de análisis: ')
    var = AnalisisSimilitud.objects.filter(informacion_analizada=tesis).count()
    print(var)
    if var >= 20:
        print('No se puede analizar más... límite alcanzado.')
        raise ValidationError("Un usuario no puede tener más de 20 análisis de tesis.")

def calcular_similitud(informacion):
    """
    Calcula el porcentaje de similitud de un texto analizado con otros documentos en la base de datos.

    :param informacion: Objeto del modelo InformacionAnalizada que contiene el texto a analizar.
    :return: Porcentaje de similitud más alto con otros documentos en la base de datos.
    """
    # Preparar el texto del documento actual
    texto_actual = f"{informacion.nombre or ''} {informacion.pregunta or ''} {informacion.objetivo or ''} {informacion.hipotesis or ''} {informacion.justificacion or ''} {informacion.problema or ''}"
    print('Informacion')
    print(texto_actual)
    print('Obtener todos los textos de la base de datos (excluyendo el actual)')
    documentos = InformacionAnalizada.objects.exclude(id=informacion.id)
    print(f"Documentos excluyendo el actual: {documentos}")

    textos_completos = [
        f"{doc.nombre or ''} {doc.pregunta or ''} {doc.objetivo or ''} {doc.hipotesis or ''} {doc.justificacion or ''} {doc.problema or ''}"
        for doc in documentos
    ]

    if not textos_completos:
        print("No hay documentos para comparar.")
        return 0  # Retorna 0% de similitud en caso de que no haya documentos.

    
    # Incluir el texto actual en la lista para calcular similitudes
    textos_completos.append(texto_actual)

    # Vectorización TF-IDF
    vectorizer = TfidfVectorizer().fit_transform(textos_completos)
    tfidf_matrix = vectorizer.toarray()

    # Calcular similitud coseno
    similitudes = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])
    print(similitudes)
    # Obtener el porcentaje de similitud más alto
    porcentaje_similitud = max(similitudes[0], default=0) * 100  # Convertir a porcentaje

    return round(porcentaje_similitud, 2)


#analizar_prueba()