from django.conf import settings

from .services import equipos_stock_bajo


def stock_bajo(request):
    """Inyecta las alertas de stock bajo en las plantillas (solo si la app está activa)."""
    if request.path.startswith('/health/'):
        return {}
    alertas = list(equipos_stock_bajo())
    return {'stock_bajo': alertas, 'stock_umbral': settings.LOW_STOCK_THRESHOLD}
