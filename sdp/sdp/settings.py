from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^xa^q$xrnjw0ugdxp-u)fm4b056g7+^+j(-k874=x=vc3%dvmx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['148.113.44.119', 'localhost', '127.0.0.1']




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'proyecto',
    'sdp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sdp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Aquí define la carpeta donde estarán tus plantillas
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'sdp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'SDP',  # Nombre de la base de datos
        'USER': 'lourdes',  # Usuario
        'PASSWORD': 'N30TTNNs.',  # Contraseña
        'HOST': 'sdpservidor.database.windows.net',  # Endpoint de la RDS
        'PORT': '',  # Puerto
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',  # Driver ODBC instalado en tu sistema
            #'TrustServerCertificate': 'yes',
        },
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/



""" # Carpeta para archivos estáticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]  
STATIC_ROOT = BASE_DIR / "staticfiles" 


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' """


#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MICROSOFT = {
    'CLIENT_ID': 'cea9dda3-2fa1-454a-95ba-32e8b7244036',  # El ID de la aplicación registrada
    'CLIENT_SECRET': '6bj8Q~4pAkSQKULECce~WrirrzCNnWCWdssA-c.t',  # El valor del secreto generado
    'AUTHORITY': 'https://login.microsoftonline.com/6b0521fd-1728-42ce-b353-7710b91f3df2',  # Tu tenant ID desde Azure
    'REDIRECT_URI': 'http://127.0.0.1:8000/home/',  # O el URL donde manejas la redirección
    'SCOPE': ['https://graph.microsoft.com/.default'],  # Permisos que necesitas
}


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

