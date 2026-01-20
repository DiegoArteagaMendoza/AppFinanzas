from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from .queryset import MovimientosQueryset
from varios.authentication import CustomJWTAuthentication
"""
Registrar Cuenta
"""

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def ingresar_movimiento(request):
    return MovimientosQueryset.ingresar_dinero(request)

"""
Buscar Cuentas
"""

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def buscar_movimiento(request):
    return MovimientosQueryset.buscar_movimientos(request)

"""
Actualizar Cuenta
"""
@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def sacar_movimiento(request):
    return MovimientosQueryset.sacar_dinero(request)