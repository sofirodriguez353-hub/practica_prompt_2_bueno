from django.contrib import admin
from .models import Familia, Usuario, CuentaBancaria, Categoria, Movimiento


@admin.register(Familia)
class FamiliaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'created_at')


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'familia')


@admin.register(CuentaBancaria)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'institucion', 'moneda', 'saldo_inicial', 'familia')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'familia')


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'monto', 'tipo', 'cuenta', 'familia')
    list_filter = ('tipo', 'fecha')
