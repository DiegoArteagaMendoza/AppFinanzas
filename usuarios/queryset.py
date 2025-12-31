from django.apps import apps
from django.db import models
from django.db.models import F, Q
from rest_framework.response import Response
from rest_framework import status
from .serializer import UsuarioSerializer
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

class UsuarioQueryset(models.QuerySet):
    
    @staticmethod
    def registrar_usuario(request):
        Usuario = apps.get_model('usuarios', 'Usuario')
        u_nombres = request.data.get("nombre")
        u_apellidos = request.data.get("apellidos")
        u_correo = request.data.get("correo")
        u_password = request.data.get("password")
        u_rut = request.data.get("rut")
        u_edad = request.data.get("edad")
        
        # if not u_nombres or not u_apellidos or not u_correo or not u_password or not u_rut or not u_edad:
        #     return Response({
        #         "error": "Todos los datos deben ser ingresados"
        #     },  status=status.HTTP_400_BAD_REQUEST)
            
        correo_obj = Usuario.objects.filter(u_correo = u_correo).first()
        if correo_obj is not None:
            return Response ({
                "error": f"El correo {u_correo} ya se encuentra registrado"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        rut_obj = Usuario.objects.filter(u_rut = u_rut).first()
        if rut_obj is not None:
            return Response ({
                "error": f"El Rut {u_rut} ya se encuentra registrado"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        data = request.data.copy()
        if 'u_password' in data:
            data['u_password'] = make_password(data['u_password'])
            
        serializer = UsuarioSerializer(data=data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                
                print(data)
                
                #usuario = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"error": "Error al crear el usuario", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def actualizar_usuario(request):
        Usuario = apps.get_model('usuarios', 'Usuario')
        u_rut = request.data.get('rut', None)
        
        try:
            usuario = Usuario.objects.get(u_rut = u_rut)
        except:
            return Response({
                'error': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"error": "Error al actualizar los datos", "detalle": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class IniciarSesion(models.QuerySet):
    
    @staticmethod
    def login(request):
        Usuario = apps.get_model('usuarios', 'Usuario')
        correo = request.data.get('u_correo', None)
        password = request.data.get('u_password', None)
        
        if not correo or not password:
            print(correo)
            print(password)
            return Response({
                "error": 'Debe proporcionar Rut o Correo y Contraseña'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:            
            if correo is not None:
                usuario = Usuario.objects.get(u_correo=correo)
                
        except Usuario.DoesNotExist:
            return Response({
                "error":'Usuario no encontrado'
            }, status=status.HTTP_403_FORBIDDEN)
            
        if check_password(password, usuario.u_password):
            serializer = UsuarioSerializer(usuario)
            return Response("Login exitoso", status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Contraseña incorrecta"},
                status=status.HTTP_401_UNAUTHORIZED
            )