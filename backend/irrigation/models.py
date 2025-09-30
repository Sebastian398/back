import uuid
import secrets
import string
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from django.conf import settings

class Sensor(models.Model):
    HUMEDAD = 'humedad'
    TEMPERATURA = 'temperatura'

    TIPO_CHOICES = [
        (HUMEDAD, 'Humedad'),
        (TEMPERATURA, 'Temperatura'),
    ]

    tipo = models.CharField(max_length=12, choices=TIPO_CHOICES)    
    valor = models.FloatField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=False)  # False: apagado, True: encendido

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.valor} - {'Activo' if self.activo else 'Inactivo'}"

class Cultivo(models.Model):
    nombre_cultivo = models.CharField(max_length=100)
    tipo_cultivo = models.CharField(max_length=100)
    numero_lotes = models.PositiveIntegerField(null=True, blank=True)
    numero_aspersores = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_cultivo} ({self.tipo_cultivo})"

class LecturaSensor(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='lecturas')
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name='lecturas', null=True, blank=True)
    valor = models.FloatField()
    fecha_registro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.sensor} - {self.valor} ({self.fecha_registro})'

class ProgramacionRiego(models.Model):
    cultivo = models.ForeignKey(Cultivo, related_name='programaciones', on_delete=models.CASCADE, null=True, blank=True)
    inicio = models.TimeField()
    duracion = models.IntegerField(help_text='Duración en minutos')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'Riego a las {self.inicio} por {self.duracion} min'


def fecha_expiracion_default():
    return timezone.now() + timedelta(days=2)

class ActivacionUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    expiracion = models.DateTimeField(default=fecha_expiracion_default)
    def esta_expirado(self):
        return timezone.now() > self.expiracion

    def __str__(self):
        return f"Token de activacion para {self.user.email}"

class RegistroRiego(models.Model):
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='registros')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    inicio = models.DateTimeField(default=timezone.now)
    duracion_minutos = models.PositiveIntegerField()
    activo = models.BooleanField(default=True)  # True durante el riego activo

    def __str__(self):
        return f"Riego en {self.sensor} iniciado {self.inicio} por {self.duracion_minutos} minutos"

class Finca(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    presentacion = models.TextField()

    def __str__(self):
        return self.nombre
class PerfilUsuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfilusuario')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

class TokenRestablecimiento(models.Model):
    """Modelo para almacenar tokens de restablecimiento de contraseña"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens_reset')
    token = models.CharField(max_length=100, unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    usado = models.BooleanField(default=False)
    expira = models.DateTimeField()
    
    class Meta:
        verbose_name = "Token de Restablecimiento"
        verbose_name_plural = "Tokens de Restablecimiento"
    
    def __str__(self):
        return f"Token para {self.user.email} - {self.token[:20]}..."
    
    def is_expired(self):
        """Verificar si el token ha expirado"""
        from django.utils import timezone
        return timezone.now() > self.expira
    
    def is_valid(self):
        """Verificar si el token es válido (no usado y no expirado)"""
        return not self.usado and not self.is_expired()
    
    @staticmethod
    def generate_token():
        """Generar un token aleatorio seguro"""
        # Generar un token de 32 caracteres con letras y números
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(32))
    
    @classmethod
    def create_for_user(cls, user):
        """Crear un nuevo token para un usuario"""
        from datetime import timedelta
        
        # Eliminar tokens anteriores no usados para este usuario
        cls.objects.filter(user=user, usado=False).delete()
        
        # Crear nuevo token
        token = cls.generate_token()
        expira = timezone.now() + timedelta(hours=24)  # Expira en 24 horas
        
        return cls.objects.create(
            user=user,
            token=token,
            expira=expira
        )