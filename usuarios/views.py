from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .queryset import UsuarioQueryset, IniciarSesion

"""
Login
"""

@api_view(['GET'])
def login(request):
    return IniciarSesion.login(request)

"""
Usuario
"""

@api_view(['POST'])
def registrar_usuario(request):
    return UsuarioQueryset.registrar_usuario(request)

@api_view(['PUT'])
def actualizar_usuario(request):
    return UsuarioQueryset.actualizar_usuario(request)