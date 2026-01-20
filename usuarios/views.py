from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from .queryset import UsuarioQueryset, IniciarSesion
from varios.authentication import CustomJWTAuthentication

"""
Login
"""

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    return IniciarSesion.login(request)

"""
Usuario
"""

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def registrar_usuario(request):
    return UsuarioQueryset.registrar_usuario(request)

@api_view(['PUT'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def actualizar_usuario(request):
    return UsuarioQueryset.actualizar_usuario(request)