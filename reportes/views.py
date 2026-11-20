import csv
from datetime import datetime

from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import render

from app.models import Equipo


def resumen(request):
    """Resumen del inventario agrupado por categoría."""
    por_categoria = (Equipo.objects.values('categoria')
                     .annotate(tipos=Count('id'), unidades=Sum('cantidad'))
                     .order_by('categoria'))
    total = Equipo.objects.aggregate(tipos=Count('id'), unidades=Sum('cantidad'))
    return render(request, 'reportes/resumen.html', {
        'por_categoria': por_categoria,
        'total_tipos': total['tipos'] or 0,
        'total_unidades': total['unidades'] or 0,
    })


def exportar_csv(request):
    """Descarga el inventario completo en CSV (compatible con Excel)."""
    nombre = f"inventario_{datetime.now():%Y%m%d_%H%M}.csv"
    respuesta = HttpResponse(content_type='text/csv; charset=utf-8')
    respuesta['Content-Disposition'] = f'attachment; filename="{nombre}"'
    respuesta.write('\ufeff')  # BOM para que Excel respete las tildes
    escritor = csv.writer(respuesta)
    escritor.writerow(['Código', 'Equipo', 'Categoría', 'Unidades', 'Registrado'])
    for e in Equipo.objects.all():
        escritor.writerow([e.codigo, e.nombre, e.categoria, e.cantidad, e.creado.strftime('%Y-%m-%d %H:%M')])
    return respuesta
