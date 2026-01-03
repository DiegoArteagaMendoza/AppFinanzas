from rest_framework import serializers
from .models import Movimientos

class MovimientosSerializer(serializers.Serializer):
    class Meta:
        model = Movimientos
        fields = [
            'm_id', 'm_tipo', 'm_monto', 'm_motivo', 'm_fecha', 'c_id', 'u_rut', 'm_persona'
        ]