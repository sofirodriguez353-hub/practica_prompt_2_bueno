from django.db import models
from django.conf import settings
from django.utils import timezone


class Familia(models.Model):
    nombre = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='miembros')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    telefono = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username


class CuentaBancaria(models.Model):
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='cuentas')
    nombre = models.CharField(max_length=120)
    institucion = models.CharField(max_length=120, blank=True)
    numero = models.CharField(max_length=64, blank=True)
    moneda = models.CharField(max_length=10, default='EUR')
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.moneda})"


class Categoria(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
        ('transfer', 'Transferencia'),
    ]
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='categorias')
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    color = models.CharField(max_length=7, default='#4A5568')
    es_default = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
        ('transfer', 'Transferencia'),
    ]
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='movimientos')
    cuenta = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE, related_name='movimientos')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(default=timezone.now, db_index=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True)
    cuenta_destino = models.ForeignKey(CuentaBancaria, on_delete=models.SET_NULL, null=True, blank=True, related_name='transferencias_recibidas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_display()} {self.monto} on {self.fecha.date()}"
