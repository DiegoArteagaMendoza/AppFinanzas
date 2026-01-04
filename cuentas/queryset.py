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

        if c_tipo == 'corriente':
            data['c_ident'] = 1
        if c_tipo == 'credito':
            data['c_ident'] = 2    
        
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
    
    @staticmethod
    def actualizar_cuenta(request):
        Cuenta = apps.get_model('cuentas', 'Cuentas')
        c_id = request.data.get('c_id', None)
        u_rut = request.data.get('u_rut', None) 
        
        print(c_id)
        print(u_rut)
    
        if not u_rut:
                return Response({
                    "error": "Debe proporcionar Rut"
                }, status=status.HTTP_400_BAD_REQUEST)
                
        try:
            if u_rut is not None:
                cuentas = Cuenta.objects.get(u_rut=u_rut, c_id=c_id)
                print(cuentas.c_tipo)
            else:
                return Response({
                    "error": "Cuenta no encontrada"
                }, status=status.HTTP_404_NOT_FOUND)
        except Cuenta.DoesNotExist:
            return Response({
                "error": "No hay cuentas para el usuario"
            }, status=status.HTTP_403_FORBIDDEN)
            
        serializer = CuentasSerializer(cuentas, data=request.data, partial=True)
        
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "error": "Error al actualizar la cuenta", "detalle": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
    @staticmethod
    def actualizar_saldo(request, c_id, monto, tipo_mov):
        if monto <= 0:
            return Response({"error": "El monto debe ser mayor a 0"}, status=status.HTTP_400_BAD_REQUEST)

        Cuenta = apps.get_model('cuentas', 'Cuentas')
        
        try:
            cuenta = Cuenta.objects.get(c_id=c_id)
        except Cuenta.DoesNotExist:
            return Response({
                "error": "No hay cuentas para el usuario"
            }, status=status.HTTP_404_NOT_FOUND)

        tipo_cuenta = cuenta.c_tipo.lower()
        
        # --- LÓGICA 1: TARJETAS DE CRÉDITO ---
        if 'credito' in tipo_cuenta:
            cupo_total = cuenta.c_cupo or 0
            usado_actual = cuenta.c_usado or 0

            if tipo_mov == 'egreso':
                if (usado_actual + monto) > cupo_total:
                    return Response({"error": "Cupo insuficiente"}, status=status.HTTP_400_BAD_REQUEST)
                cuenta.c_usado = usado_actual + monto

            elif tipo_mov == 'ingreso':
                if (usado_actual - monto) < 0:
                    cuenta.c_usado = 0
                else:
                    cuenta.c_usado = usado_actual - monto
                    
        # --- LÓGICA 2: DÉBITO / CORRIENTE / VISTA ---
        else:
            disponible = cuenta.c_disponible or 0
            
            if tipo_mov == 'ingreso':
                cuenta.c_disponible = disponible + monto
                
            elif tipo_mov == 'egreso':
                if disponible >= monto:
                    cuenta.c_disponible = disponible - monto
                else:
                    # --- LÓGICA EXTRA: LÍNEA DE CRÉDITO ---
                    if cuenta.c_lineaCredito:
                        faltante = monto - disponible
                        linea_cupo = cuenta.c_lineaCupo or 0
                        linea_usado = cuenta.c_lineaUsado or 0
                        
                        if (linea_usado + faltante) <= linea_cupo:
                            cuenta.c_disponible = 0
                            cuenta.c_lineaUsado = linea_usado + faltante
                        else:
                            return Response({"error": "Saldo y línea de crédito insuficientes"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"error": "Saldo insuficiente"}, status=status.HTTP_400_BAD_REQUEST)

        cuenta.save()

        return Response({
            "mensaje": "Saldo actualizado correctamente",
            "cuenta": cuenta.c_nombre,
            "nuevo_saldo_disponible": cuenta.c_disponible,
            "nuevo_saldo_usado": cuenta.c_usado
        }, status=status.HTTP_200_OK)
    
    @staticmethod
    def buscar_cuentas(request):
        Cuenta = apps.get_model('cuentas', 'Cuentas')
        u_rut = request.data.get('u_rut', None)
        c_tipo = request.data.get('c_tipo', None)
        
        print(c_tipo)
                
        if not u_rut:
            return Response({
                "error": "Debe proporcionar Rut"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            if u_rut is not None:
                if c_tipo is not None and c_tipo != "None":
                    cuentas = Cuenta.objects.all().filter(u_rut=u_rut).filter(c_tipo=c_tipo)
                else:
                    cuentas = Cuenta.objects.all().filter(u_rut=u_rut)
        except Cuenta.DoesNotExist:
            return Response({
                "error": "No hay cuentas para el usuario"
            }, status=status.HTTP_403_FORBIDDEN)
            
        # serializer = CuentasSerializer(cuentas, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CuentasSerializer(cuentas, many=True)
        
        # 1. Obtenemos los datos serializados (es una lista de diccionarios)
        data = serializer.data 
        
        # 2. Iteramos sobre cada cuenta para inyectar el campo extra
        for cuenta in data:
            # Validamos que los valores existan (por si vienen nulos de la BD)
            cupo = cuenta.get('c_cupo') or 0
            usado = cuenta.get('c_usado') or 0
            tipo = cuenta.get('c_tipo', '').lower()

            if 'credito' in tipo:
                # Calculamos el disponible de la tarjeta
                cuenta['saldo_visual_disponible'] = cupo - usado
            else:
                # Para débito/corriente, el disponible es directo
                cuenta['saldo_visual_disponible'] = cuenta.get('c_disponible')

        return Response(data, status=status.HTTP_200_OK)
    
    
    @staticmethod
    def buscar_cuenta_id(request):
        Cuenta = apps.get_model('cuentas', 'Cuentas')
        c_id = request.data.get('c_id', None)
        
        print(c_id)
                        
        if not c_id:
            return Response({
                "error": "Debe proporcionar el id"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            if c_id is not None:
                cuentas = Cuenta.objects.get(c_id=c_id)
        except Cuenta.DoesNotExist:
            return Response({
                "error": "Cuenta no encontrada"
            }, status=status.HTTP_403_FORBIDDEN)
            
        serializer = CuentasSerializer(cuentas)
        return Response(serializer.data, status=status.HTTP_200_OK)