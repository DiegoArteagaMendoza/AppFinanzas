from django.urls import path
from . import views

urlpatterns = [
    path('registrar', views.crear_cuenta, name='registrar'),
    path('buscar', views.buscar_cuenta, name='buscar'),
]
