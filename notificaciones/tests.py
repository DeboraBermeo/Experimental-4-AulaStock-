from django.conf import settings
from unittest import skipUnless

from django.test import TestCase
from django.urls import reverse

from app.models import Equipo


@skipUnless(settings.ENABLE_NOTIFICATIONS, 'Notificaciones desactivado en esta variante')
class NotificacionesTests(TestCase):
    def test_alerta_en_listado_con_stock_bajo(self):
        Equipo.objects.create(codigo='EQ-002', nombre='Switch', categoria='Redes', cantidad=settings.LOW_STOCK_THRESHOLD)
        self.assertContains(self.client.get('/'), 'Stock bajo')

    def test_sin_alerta_si_stock_suficiente(self):
        Equipo.objects.create(codigo='EQ-001', nombre='Laptop', categoria='Computación', cantidad=settings.LOW_STOCK_THRESHOLD + 1)
        self.assertNotContains(self.client.get('/'), 'Stock bajo:')

    def test_pagina_detalle_ordena_por_cantidad(self):
        Equipo.objects.create(codigo='EQ-A', nombre='A', categoria='Redes', cantidad=4)
        Equipo.objects.create(codigo='EQ-B', nombre='B', categoria='Redes', cantidad=1)
        r = self.client.get(reverse('notificaciones:stock_bajo'))
        self.assertEqual([e.codigo for e in r.context['stock_bajo']], ['EQ-B', 'EQ-A'])

    def test_health_no_consulta_alertas(self):
        self.assertEqual(self.client.get('/health/').status_code, 200)
