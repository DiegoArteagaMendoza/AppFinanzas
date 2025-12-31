from django.apps import apps
from django.db import models
from django.db.models import F, Q
from rest_framework.response import Response
from rest_framework import status
from .serializer import CuentasSerializer
from django.conf import settings

class CuentasQueryset(models.QuerySet):
    
    @staticmethod
    def registrar_cuenta(request):
        Cuenta = apps.get_model('cuentas', 'Cuentas')
        c_tipo = request.data.get("c_tipo")
        c_banco = request.data.get("c_banco")
        c_nombre = request.data.get("c_nombre")
        u_rut = request.data.get("u_rut")
        
        if not c_tipo:
            return Response({
                "error": "Es necesario el tipo de cuenta"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not c_banco:
            return Response({
                "error": "Es necesario el banco"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if not c_nombre:
            return Response({
                "error": "Es necesario el nombre de cuenta"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        if 'u_rut' not in data:
            return Response({
                "error": "Error en la información"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = CuentasSerializer(data=data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                print(data)
                print(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "error": "Error al crear la cuenta"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # @staticmethod
    # def actualizar_cuenta(request):
    #     Cuenta = apps.get_model('cuentas', 'Cuenta')
    
    @staticmethod
    def buscar_cuentas(request):
        Cuenta = apps.get_model('cuentas', 'Cuenta')
        u_rut = request.data.get('u_rut', None)
        
        if not u_rut:
            return Response({
                "error": "Debe proporcionar Rut"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            if u_rut is not None:
                cuentas = Cuenta.objects.all(u_rut=u_rut)
        except Cuenta.DoesNotExist:
            return Response({
                "error": "No hay cuentas para el usuario"
            }, status=status.HTTP_403_FORBIDDEN)
            
        serializer = CuentasSerializer(cuentas)
        return Response(serializer, status=status.HTTP_200_OK)