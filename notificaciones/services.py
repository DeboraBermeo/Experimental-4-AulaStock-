from django.conf import settings

from app.models import Equipo


def equipos_stock_bajo():
    """Equipos cuya cantidad es igual o menor al umbral configurado."""
    return Equipo.objects.filter(cantidad__lte=settings.LOW_STOCK_THRESHOLD).order_by('cantidad', 'codigo')
