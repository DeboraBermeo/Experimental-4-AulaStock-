from django.urls import path
from . import views
urlpatterns = [path('', views.listado, name='lista'), path('equipos/nuevo/', views.guardar, name='nuevo'), path('equipos/<int:pk>/editar/', views.guardar, name='editar'), path('equipos/<int:pk>/eliminar/', views.eliminar, name='eliminar'), path('health/', views.health, name='health')]
