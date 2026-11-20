"""Definición de las variantes de la línea de productos AulaStock.

Cada variante es un diccionario de características (feature flags).
Para añadir una característica nueva:
  1. agregue su bandera aquí en cada variante,
  2. léala en settings.py,
  3. úsela en urls.py / plantillas con un condicional.
"""

# Variante A: sistema básico (solo el núcleo de inventario).
PRODUCT_A = {
    'NAME': 'AulaStock Básico',
    'ENABLE_REPORTS': False,
    'ENABLE_NOTIFICATIONS': False,
}

# Variante B: sistema completo (núcleo + reportes + notificaciones).
PRODUCT_B = {
    'NAME': 'AulaStock Completo',
    'ENABLE_REPORTS': True,
    'ENABLE_NOTIFICATIONS': True,
}

VARIANTS = {'A': PRODUCT_A, 'B': PRODUCT_B}
DEFAULT_VARIANT = 'B'
