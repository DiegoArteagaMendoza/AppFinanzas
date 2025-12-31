from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'u_id', 'u_nombres', 'u_apellidos', 'u_correo', 'u_password', 'u_rut', 'u_edad'
        ]
        # read_only_fields = ('u_id')