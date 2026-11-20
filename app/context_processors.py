from django.conf import settings


def features(request):
    """Expone la variante y las banderas de características a todas las plantillas."""
    return {
        'features': {
            'reports': settings.ENABLE_REPORTS,
            'notifications': settings.ENABLE_NOTIFICATIONS,
        },
        'product_variant': settings.PRODUCT_VARIANT,
        'product_name': settings.PRODUCT_NAME,
        'app_version': settings.APP_VERSION,
    }
