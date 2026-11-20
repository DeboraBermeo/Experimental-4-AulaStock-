from django.conf import settings
from django.contrib import messages
from django.db import connection
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import EquipoForm
from .models import Equipo

def listado(request):
    equipos = Equipo.objects.all()
    return render(request, 'app/lista.html', {'equipos': equipos, 'total': equipos.aggregate(n=Sum('cantidad'))['n'] or 0})

def guardar(request, pk=None):
    equipo = get_object_or_404(Equipo, pk=pk) if pk else None
    form = EquipoForm(request.POST or None, instance=equipo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Equipo guardado correctamente')
        return redirect('lista')
    return render(request, 'app/form.html', {'form': form, 'editando': equipo is not None})

@require_POST
def eliminar(request, pk):
    get_object_or_404(Equipo, pk=pk).delete()
    messages.success(request, 'Equipo eliminado correctamente')
    return redirect('lista')

def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
    except Exception:
        return JsonResponse({'status': 'unavailable'}, status=503)
    return JsonResponse({'status': 'ok', 'app': 'AulaStock', 'version': settings.APP_VERSION, 'variant': settings.PRODUCT_VARIANT})
