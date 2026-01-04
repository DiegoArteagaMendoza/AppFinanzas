from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from .queryset import CuentasQueryset
from varios.authentication import CustomJWTAuthentication
"""
Registrar Cuenta
"""

@api_view(['POST'])
<<<<<<< HEAD
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
=======
#@authentication_classes([CustomJWTAuthentication])
#@permission_classes([IsAuthenticated])
>>>>>>> devCuentas
def crear_cuenta(request):
    return CuentasQueryset.registrar_cuenta(request)

"""
Buscar Cuentas
"""

@api_view(['GET'])
<<<<<<< HEAD
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
=======
#@authentication_classes([CustomJWTAuthentication])
#@permission_classes([IsAuthenticated])
>>>>>>> devCuentas
def buscar_cuenta(request):
    return CuentasQueryset.buscar_cuentas(request)

@api_view(['GET'])
#@authentication_classes([CustomJWTAuthentication])
#@permission_classes([IsAuthenticated])
def buscar_cuenta_id(request):
    return CuentasQueryset.buscar_cuenta_id(request)

"""
Actualizar Cuenta
"""
@api_view(['PUT'])
<<<<<<< HEAD
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
=======
#@authentication_classes([CustomJWTAuthentication])
#@permission_classes([IsAuthenticated])
>>>>>>> devCuentas
def actualizar_cuenta(request):
    return CuentasQueryset.actualizar_cuenta(request)