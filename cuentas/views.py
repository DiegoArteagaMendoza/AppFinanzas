from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .queryset import CuentasQueryset

"""
Registrar Cuenta
"""

@api_view(['POST'])
def crear_cuenta(request):
    return CuentasQueryset.registrar_cuenta(request)

"""
Buscar Cuentas
"""

@api_view(['GET'])
def buscar_cuenta(request):
    return CuentasQueryset.buscar_cuentas(request)