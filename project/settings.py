import os
from pathlib import Path
from .config_product import DEFAULT_VARIANT, VARIANTS
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Línea de productos: variante activa -----------------------------------
# Se elige con la variable de entorno PRODUCT_VARIANT (A = básico, B = completo).
PRODUCT_VARIANT = os.getenv('PRODUCT_VARIANT', DEFAULT_VARIANT).strip().upper()
if PRODUCT_VARIANT not in VARIANTS:
    raise RuntimeError(f"PRODUCT_VARIANT inválida: {PRODUCT_VARIANT!r}. Use una de {sorted(VARIANTS)}")
_PRODUCT = VARIANTS[PRODUCT_VARIANT]
PRODUCT_NAME = _PRODUCT['NAME']
ENABLE_REPORTS = _PRODUCT['ENABLE_REPORTS']
ENABLE_NOTIFICATIONS = _PRODUCT['ENABLE_NOTIFICATIONS']
# Una unidad igual o menor a este valor se considera "stock bajo".
LOW_STOCK_THRESHOLD = int(os.getenv('LOW_STOCK_THRESHOLD', '5'))
try:
    APP_VERSION = (BASE_DIR / 'VERSION').read_text().strip()
except OSError:
    APP_VERSION = '0.0.0'
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = os.getenv('DJANGO_DEBUG', '0') == '1'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,web').split(',')
INSTALLED_APPS = ['django.contrib.contenttypes', 'django.contrib.auth', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'app']
# Apps opcionales: solo se cargan si la variante las incluye.
if ENABLE_REPORTS:
    INSTALLED_APPS.append('reportes')
if ENABLE_NOTIFICATIONS:
    INSTALLED_APPS.append('notificaciones')
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware']
ROOT_URLCONF = 'project.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.request', 'django.contrib.messages.context_processors.messages', 'app.context_processors.features']}}]
if ENABLE_NOTIFICATIONS:
    TEMPLATES[0]['OPTIONS']['context_processors'].append('notificaciones.context_processors.stock_bajo')
WSGI_APPLICATION = 'project.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': os.getenv('POSTGRES_DB', 'aulastock'), 'USER': os.getenv('POSTGRES_USER', 'aulastock'), 'PASSWORD': os.environ['POSTGRES_PASSWORD'], 'HOST': os.getenv('POSTGRES_HOST', 'db'), 'PORT': os.getenv('POSTGRES_PORT', '5432')}}
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
