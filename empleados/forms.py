from django import forms
from django.contrib.auth.models import User
from .models import Empleado
class EmpleadoRegistroForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label = 'Usuario',
        widget = forms.TextInput(attrs = {
            'placeholder': 'ABC123',
            'class': 'perfil-input'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=False,
        label='Nombre',
        widget=forms.TextInput(attrs={
            'placeholder':'Juan',
            'class': 'perfil-input'
        })
    )
    last_name=forms.CharField(
        max_length=100,
        required=False,
        label='Apellido',
        widget=forms.TextInput(attrs={
            'placeholder': 'Pérez',
            'class': 'perfil-input'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'empleado@dana.com',
            'class': 'perfil-input'
        })
    )
    password = forms.CharField(
        label = 'Contraseña',
        widget = forms.PasswordInput(attrs={
            'placeholder': '********',
            'class': 'perfil-input'
        })
    )

    legajo = forms.CharField(
        max_length=20,
        label='Legajo',
        widget = forms.TextInput(attrs={
            'placeholder': 'EMP001',
            'class': 'perfil-input'
        })
    )

    sector = forms.ChoiceField(
        choices = Empleado.SECTOR_CHOICES,
        label = 'Sector',
        widget = forms.Select(attrs={
            'class': 'perfil-input'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Ese nombre de usuario ya existe. Por favor elige otro.')
        return username
    
    def clean_legajo(self):
        legajo = self.cleaned_data.get('legajo')
        if Empleado.objects.filter(legajo=legajo).exists():
            raise forms.ValidationError('Ese legajo ya está registrado.')
        return legajo