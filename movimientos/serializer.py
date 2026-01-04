from rest_framework import serializers
from .models import Movimientos

class MovimientosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimientos
        fields = [
            'm_id', 'm_tipo', 'm_monto', 'm_motivo', 'm_fecha', 'm_persona', 'c_id', 'u_rut', 'm_persona'
        ]