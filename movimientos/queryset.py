from django.apps import apps
from django.db import models
from django.db.models import F, Q
from rest_framework.response import Response
from rest_framework import status
from .serializer import MovimientosSerializer
from django.conf import settings

class MovimientosQueryset(models.QuerySet):
    
    @staticmethod
    def ingresar_dinero(request):
        Movimiento = apps.get_model('movimientos', 'Movimientos')
        m_tipo = request.data.get('m_tipo')
        m_monto = request.data.get('m_monto')
        m_fecha = request.data.get('m_fecha')
        m_persona = request.data.get('m_persona')
        
        if not m_tipo or not m_monto or not m_fecha:
            return Response({
                "error": "Datos incompletos"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        data = request.data.copy()
        
        if m_persona == 'propio':
            data['m_persona'] = 1
        if m_persona == 'otro':
            data['m_persona'] = 2
            
        serializer = MovimientosSerializer(data=data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                # ACTUALIZAR SALDO
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "error": f"Error al ingresar movimiento {e}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)