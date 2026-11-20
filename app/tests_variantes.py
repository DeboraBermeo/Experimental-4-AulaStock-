"""Pruebas de la línea de productos: se adaptan a la variante activa (PRODUCT_VARIANT)."""
from django.conf import settings
from django.apps import apps
from django.test import TestCase
from django.urls import NoReverseMatch, reverse

from project.config_product import VARIANTS


class VariantesTests(TestCase):
    def test_banderas_coinciden_con_config_product(self):
        cfg = VARIANTS[settings.PRODUCT_VARIANT]
        self.assertEqual(settings.ENABLE_REPORTS, cfg['ENABLE_REPORTS'])
        self.assertEqual(settings.ENABLE_NOTIFICATIONS, cfg['ENABLE_NOTIFICATIONS'])

    def test_apps_instaladas_segun_variante(self):
        self.assertEqual(apps.is_installed('reportes'), settings.ENABLE_REPORTS)
        self.assertEqual(apps.is_installed('notificaciones'), settings.ENABLE_NOTIFICATIONS)

    def test_urls_segun_variante(self):
        for nombre, activa in (('reportes:resumen', settings.ENABLE_REPORTS),
                               ('notificaciones:stock_bajo', settings.ENABLE_NOTIFICATIONS)):
            if activa:
                self.assertTrue(reverse(nombre))
            else:
                with self.assertRaises(NoReverseMatch):
                    reverse(nombre)

    def test_rutas_opcionales_inexistentes_si_estan_apagadas(self):
        if not settings.ENABLE_REPORTS:
            self.assertEqual(self.client.get('/reportes/').status_code, 404)
        if not settings.ENABLE_NOTIFICATIONS:
            self.assertEqual(self.client.get('/notificaciones/stock-bajo/').status_code, 404)

    def test_interfaz_muestra_variante_y_menu(self):
        html = self.client.get('/').content.decode()
        self.assertIn(f'Variante {settings.PRODUCT_VARIANT}', html)
        self.assertEqual('Exportar CSV' in html, settings.ENABLE_REPORTS)
        self.assertEqual('>Reportes<' in html, settings.ENABLE_REPORTS)
        self.assertEqual('>Alertas' in html, settings.ENABLE_NOTIFICATIONS)

    def test_health_informa_variante(self):
        self.assertEqual(self.client.get('/health/').json()['variant'], settings.PRODUCT_VARIANT)
