from django.core.management.base import BaseCommand
from app.models import Equipo
class Command(BaseCommand):
    help = 'Carga datos de ejemplo identificados, sin duplicarlos'
    def handle(self, *args, **options):
        for codigo, nombre, categoria, cantidad in [('EQ-001', 'Laptop de laboratorio', 'Computación', 12), ('EQ-002', 'Switch de 24 puertos', 'Redes', 3), ('EQ-003', 'Proyector multimedia', 'Accesorios', 2)]:
            Equipo.objects.get_or_create(codigo=codigo, defaults=dict(nombre=nombre, categoria=categoria, cantidad=cantidad))
        self.stdout.write(self.style.SUCCESS('Datos de ejemplo disponibles: 3 tipos, 17 unidades si la base estaba vacía'))
