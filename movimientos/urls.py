from django.urls import path
from . import views

urlpatterns = [
    path('ingresar', views.ingresar_movimiento, name='ingresar'),
    path('buscar', views.buscar_movimiento, name='buscar'),
    path('sacar', views.sacar_movimiento, name='sacar'),
]