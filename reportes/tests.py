from django.conf import settings
from unittest import skipUnless

from django.test import TestCase
from django.urls import reverse

from app.models import Equipo


@skipUnless(settings.ENABLE_REPORTS, 'Reportes desactivado en esta variante')
class ReportesTests(TestCase):
    def setUp(self):
        Equipo.objects.create(codigo='EQ-001', nombre='Laptop', categoria='Computación', cantidad=12)
        Equipo.objects.create(codigo='EQ-002', nombre='Switch', categoria='Redes', cantidad=3)

    def test_csv_descarga(self):
        r = self.client.get(reverse('reportes:exportar_csv'))
        self.assertEqual(r.status_code, 200)
        self.assertIn('text/csv', r['Content-Type'])
        self.assertIn('attachment', r['Content-Disposition'])
        texto = r.content.decode('utf-8')
        self.assertIn('EQ-001', texto)
        self.assertIn('Computación', texto)

    def test_resumen_totales(self):
        r = self.client.get(reverse('reportes:resumen'))
        self.assertEqual(r.context['total_unidades'], 15)
        self.assertEqual(r.context['total_tipos'], 2)

    def test_resumen_vacio(self):
        Equipo.objects.all().delete()
        self.assertContains(self.client.get(reverse('reportes:resumen')), 'No hay datos')
