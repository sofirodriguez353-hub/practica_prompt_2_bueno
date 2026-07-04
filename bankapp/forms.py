from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Movimiento, CuentaBancaria, Categoria, Familia, Usuario
from django.db import transaction


class SignupForm(UserCreationForm):
    family_name = forms.CharField(max_length=150, label='Nombre de la familia')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)
        family = Familia.objects.create(nombre=self.cleaned_data['family_name'])
        Usuario.objects.create(user=user, familia=family)
        return user


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['fecha', 'monto', 'tipo', 'cuenta', 'categoria', 'cuenta_destino', 'descripcion']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get('tipo')
        cuenta_destino = cleaned.get('cuenta_destino')
        cuenta = cleaned.get('cuenta')
        if tipo == 'transfer':
            if not cuenta_destino:
                raise forms.ValidationError('Transferencia requiere cuenta destino')
            if cuenta_destino == cuenta:
                raise forms.ValidationError('Cuenta destino debe ser distinta')
        return cleaned
