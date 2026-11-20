# Comprobación auxiliar sin PostgreSQL; Docker y CI usan project.settings.
import os
os.environ.setdefault('DJANGO_SECRET_KEY', 'local-check-only-not-for-deployment')
os.environ.setdefault('POSTGRES_PASSWORD', 'unused-local-check')
from .settings import *
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'local.sqlite3'}}
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
