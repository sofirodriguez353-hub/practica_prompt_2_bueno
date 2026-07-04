from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignupForm, MovimientoForm
from .models import Movimiento, CuentaBancaria
from django.db import transaction


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso. Bienvenido!')
            return redirect('feed')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def feed(request):
    familia = request.user.perfil.familia
    movimientos = Movimiento.objects.filter(familia=familia).select_related('cuenta', 'categoria', 'creado_por')

    # Calcular saldo por cuenta
    cuentas = CuentaBancaria.objects.filter(familia=familia)
    saldo_total = sum([c.saldo_inicial for c in cuentas])
    # Ajuste: sumar movimientos (ingreso/gasto) a saldo_total
    for m in movimientos:
        if m.tipo == 'ingreso':
            saldo_total += m.monto
        elif m.tipo == 'gasto':
            saldo_total -= m.monto
        elif m.tipo == 'transfer':
            # transfer: restar de cuenta origen, sumar a destino (no doble contar global)
            saldo_total += 0

    return render(request, 'bankapp/feed.html', {'movimientos': movimientos, 'saldo_total': saldo_total, 'cuentas': cuentas})


@login_required
def movimiento_create(request):
    familia = request.user.perfil.familia
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.familia = familia
            movimiento.creado_por = request.user
            movimiento.save()
            messages.success(request, 'Movimiento creado')
            return redirect('feed')
    else:
        form = MovimientoForm()
        # limitar cuentas y categorias al contexto de la familia
        form.fields['cuenta'].queryset = CuentaBancaria.objects.filter(familia=familia)
        form.fields['categoria'].queryset = form.fields['categoria'].queryset.filter(familia=familia)
        form.fields['cuenta_destino'].queryset = CuentaBancaria.objects.filter(familia=familia)
    return render(request, 'bankapp/movimiento_form.html', {'form': form})


@login_required
def movimiento_update(request, pk):
    familia = request.user.perfil.familia
    movimiento = get_object_or_404(Movimiento, pk=pk, familia=familia)
    if request.method == 'POST':
        form = MovimientoForm(request.POST, instance=movimiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimiento actualizado')
            return redirect('feed')
    else:
        form = MovimientoForm(instance=movimiento)
        form.fields['cuenta'].queryset = CuentaBancaria.objects.filter(familia=familia)
        form.fields['categoria'].queryset = form.fields['categoria'].queryset.filter(familia=familia)
        form.fields['cuenta_destino'].queryset = CuentaBancaria.objects.filter(familia=familia)
    return render(request, 'bankapp/movimiento_form.html', {'form': form, 'movimiento': movimiento})


@login_required
def movimiento_delete(request, pk):
    familia = request.user.perfil.familia
    movimiento = get_object_or_404(Movimiento, pk=pk, familia=familia)
    if request.method == 'POST':
        movimiento.delete()
        messages.success(request, 'Movimiento eliminado')
        return redirect('feed')
    return render(request, 'bankapp/movimiento_confirm_delete.html', {'movimiento': movimiento})
