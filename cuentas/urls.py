from django.urls import path
from . import views

urlpatterns = [
    path('registrar', views.crear_cuenta, name='registrar'),
    path('buscar', views.buscar_cuenta, name='buscar'),
    path('actualizar', views.actualizar_cuenta, name='actualizar'),
    path('actualizar/saldo', views.actualizar_cuenta, name='actualizar saldo'),
    path('buscar/unica', views.buscar_cuenta_id, name='buscar unica'),
]
