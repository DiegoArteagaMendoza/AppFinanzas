from rest_framework import serializers
from .models import Cuentas

class CuentasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuentas
        fields = [
            'c_id', 'c_tipo', 'c_banco', 'c_nombre', 'u_rut', 'c_estado', 'c_cupo', 'c_usado', 'c_disponible', 'c_lineaCredito', 'c_lineaCupo', 'c_lineaUsado'
        ]
        