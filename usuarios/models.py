from django.db import models

# Create your models here.
class Usuario(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_nombres = models.CharField(max_length=100)
    u_apellidos = models.CharField(max_length=100)
    u_correo = models.EmailField(max_length=100, unique=True)
    u_password = models.CharField(max_length=100)
    u_rut = models.CharField(max_length=12, unique=True)
    u_edad = models.IntegerField()
    
    def __str__(self):
        return f"{self.u_nombres} {self.u_apellidos}"
        
class Perfil(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    p_foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    
    def __str__(self):
        return f"Perfil de {self.p_usuario.u_nombres} {self.p_usuario.u_apellidos}"