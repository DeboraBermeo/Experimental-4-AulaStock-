from django.shortcuts import render


def stock_bajo(request):
    # La lista llega por el context processor de esta app.
    return render(request, 'notificaciones/stock_bajo.html')
