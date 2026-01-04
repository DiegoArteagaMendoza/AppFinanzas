from django.apps import apps
from django.db import models
from django.db.models import F, Q
from rest_framework.response import Response
from rest_framework import status
from .serializer import MovimientosSerializer
from django.conf import settings
from .tipoPersonas import tipo_personas
from cuentas.queryset import CuentasQueryset

class MovimientosQueryset(models.QuerySet):
    
    @staticmethod
    def buscar_movimientos(request):
        Movimiento = apps.get_model('movimientos', 'Movimientos')
        m_tipo = request.data.get('m_tipo', None)
    
        movimientos_qs = Movimiento.objects.all()
        if m_tipo is not None:
            movimientos_qs = movimientos_qs.filter(m_tipo=m_tipo)
        
        if not movimientos_qs.exists():
             return Response({"error": "No hay movimientos"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovimientosSerializer(movimientos_qs, many=True)
        data_serializada = serializer.data

        lista_final = []

        for item in data_serializada:
            item_modificado = dict(item)
            id_persona = int(item_modificado.get('m_persona', 0))
            texto_persona = tipo_personas.get(id_persona, "Desconocido")
            item_modificado['m_persona'] = texto_persona
            lista_final.append(item_modificado)

        return Response(lista_final, status=status.HTTP_200_OK)
    
    @staticmethod
    def ingresar_dinero(request):
        Movimiento = apps.get_model('movimientos', 'Movimientos')
        m_tipo = request.data.get('m_tipo')
        m_monto = request.data.get('m_monto')
        m_fecha = request.data.get('m_fecha')
        m_persona = request.data.get('m_persona')
        c_id = request.data.get('c_id')
        
        print(request)
        
        if not m_tipo or not m_monto or not m_fecha:
            return Response({
                "error": "Datos incompletos"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        data = request.data.copy()
        
        if m_persona == 'propio':
            data['m_persona'] = "1"
        if m_persona == 'otro':
            data['m_persona'] = "2"
            
        serializer = MovimientosSerializer(data=data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                # ACTUALIZAR SALDO SUMAR DINERO MEDIANTE RESPUESTA SATISFACTORIA, MANDA ACTUALIZAR
                CuentasQueryset.actualizar_saldo(request, c_id, m_monto, m_tipo)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "error": f"Error al ingresar movimiento {e}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def sacar_dinero(request):
        Movimiento = apps.get_model('movimientos', 'Movimientos')
        m_tipo = request.data.get('m_tipo')
        m_monto = request.data.get('m_monto')
        m_fecha = request.data.get('m_fecha')
        m_persona = request.data.get('m_persona')
        c_id = request.data.get('c_id')
        
        if not m_tipo or not m_monto or not m_fecha:
            return Response({
                "error": "Datos incompletos"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        data = request.data.copy()
        
        if m_persona == 'cajero':
            data['m_persona'] = "3"
        if m_persona == 'transferencia':
            data['m_persona'] = "4"
        if m_persona == 'pago':
            data['m_persona'] == "5"
        if m_persona == 'compra':
            data['m_persona'] == "6"
            
        serializer = MovimientosSerializer(data=data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                # ACTUALIZAR SALDO RESTAR DINERO MEDIANTE RESPUESTA SATISFACTORIA, MANDA ACTUALIZAR
                CuentasQueryset.actualizar_saldo(request, c_id, m_monto, m_tipo)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "error": f"Error al ingresar movimiento {e}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)