from django.db import models

# Create your models here.
class Cuentas(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_tipo = models.CharField(max_length=50, null=False)
    c_banco = models.CharField(max_length=50, null=False)
    c_nombre = models.CharField(max_length=100, null=False)
    u_rut = models.CharField(max_length=12, null=False)
    c_estado = models.BooleanField(default=True)
    
    # credito seccion
    c_cupo = models.IntegerField(null=True, blank=True)
    c_usado = models.IntegerField(null=True, blank=True)
    
    # corriente / debito seccion
    c_disponible = models.IntegerField(null=True, blank=True)
    c_lineaCredito = models.BooleanField(null=True, blank=True, default=False)
    c_lineaCupo = models.IntegerField(null=True, blank=True)
    c_lineaUsado = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.c_nombre} {self.c_tipo}"