from django.db import models
from django.core.validators import MinValueValidator
class Equipo(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=[('Computación', 'Computación'), ('Redes', 'Redes'), ('Accesorios', 'Accesorios')])
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    creado = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['codigo']
        constraints = [models.CheckConstraint(condition=models.Q(cantidad__gte=1), name='cantidad_minima_uno')]
    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
