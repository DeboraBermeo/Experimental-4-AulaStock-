from django.urls import path

from . import views

app_name = 'notificaciones'
urlpatterns = [path('stock-bajo/', views.stock_bajo, name='stock_bajo')]
