from django.db import models

# Create your models here.
class Movimientos(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_tipo = models.CharField(max_length=50, null=False, blank=False)
    m_monto = models.IntegerField(null=False, blank=False)
    m_motivo = models.TextField()
    m_fecha = models.DateField(null=False, blank=False)
    m_persona = models.CharField(null=False, blank=False, default="0")
    c_id = models.IntegerField(null=False, blank=False)
    u_rut = models.CharField(max_length=12, null=False, blank=False)
    
    def __str__(self):
        return f"{self.m_tipo} {self.m_monto}"