from django.conf import settings
from django.urls import include, path

urlpatterns = [path('', include('app.urls'))]

# Rutas de las características opcionales: solo existen si la variante las activa.
if settings.ENABLE_REPORTS:
    urlpatterns.append(path('reportes/', include('reportes.urls')))
if settings.ENABLE_NOTIFICATIONS:
    urlpatterns.append(path('notificaciones/', include('notificaciones.urls')))
