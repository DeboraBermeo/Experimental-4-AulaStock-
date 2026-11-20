from unittest.mock import patch
from django.db import OperationalError
from django.test import TestCase, Client
from django.urls import reverse
from .models import Equipo
class InventarioTests(TestCase):
    def setUp(self):
        self.data = {'codigo': 'EQ-001', 'nombre': 'Laptop', 'categoria': 'Computación', 'cantidad': 12}
    def test_lista_vacia(self):
        self.assertContains(self.client.get('/'), 'Todavía no hay equipos')
    def test_crear_equipo(self):
        self.assertRedirects(self.client.post(reverse('nuevo'), self.data), '/')
        self.assertEqual(Equipo.objects.get().cantidad, 12)
    def test_codigo_duplicado(self):
        Equipo.objects.create(**self.data)
        self.assertEqual(self.client.post(reverse('nuevo'), self.data).status_code, 200)
        self.assertEqual(Equipo.objects.count(), 1)
    def test_cantidad_cero_rechazada(self):
        self.data['cantidad'] = 0
        self.assertContains(self.client.post(reverse('nuevo'), self.data), 'mayor o igual a 1')
        self.assertFalse(Equipo.objects.exists())
    def test_cantidad_negativa_rechazada(self):
        self.data['cantidad'] = -2
        self.client.post(reverse('nuevo'), self.data)
        self.assertFalse(Equipo.objects.exists())
    def test_campos_obligatorios(self):
        self.client.post(reverse('nuevo'), {})
        self.assertFalse(Equipo.objects.exists())
    def test_normaliza_codigo(self):
        self.data['codigo'] = 'eq-001'
        self.client.post(reverse('nuevo'), self.data)
        self.assertEqual(Equipo.objects.get().codigo, 'EQ-001')
    def test_editar(self):
        e = Equipo.objects.create(**self.data)
        self.data['cantidad'] = 8
        self.assertRedirects(self.client.post(reverse('editar', args=[e.pk]), self.data), '/')
        e.refresh_from_db()
        self.assertEqual(e.cantidad, 8)
    def test_eliminar(self):
        e = Equipo.objects.create(**self.data)
        self.assertRedirects(self.client.post(reverse('eliminar', args=[e.pk])), '/')
        self.assertFalse(Equipo.objects.exists())
    def test_eliminar_no_acepta_get(self):
        e = Equipo.objects.create(**self.data)
        self.assertEqual(self.client.get(reverse('eliminar', args=[e.pk])).status_code, 405)
        self.assertTrue(Equipo.objects.exists())
    def test_inexistente(self):
        self.assertEqual(self.client.get(reverse('editar', args=[999])).status_code, 404)
    def test_health(self):
        self.assertEqual(self.client.get('/health/').json()['status'], 'ok')
    def test_health_error(self):
        with patch('app.views.connection.cursor', side_effect=OperationalError('offline')):
            self.assertEqual(self.client.get('/health/').status_code, 503)
    def test_csrf(self):
        self.assertEqual(Client(enforce_csrf_checks=True).post(reverse('nuevo'), self.data).status_code, 403)
    def test_total_unidades(self):
        Equipo.objects.create(**self.data)
        self.assertEqual(self.client.get('/').context['total'], 12)
