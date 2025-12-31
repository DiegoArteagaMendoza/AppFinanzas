from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('registro', views.registrar_usuario, name='registrar_usuario'),
    path('actualizar', views.actualizar_usuario, name='actualizar_usuario'),
]