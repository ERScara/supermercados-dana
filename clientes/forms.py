from django import forms
from django.contrib.auth.models import User
from .models import Cliente, Comentario
from django.contrib.auth.forms import UserCreationForm
from productos.models import Categoria

class PerfilForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        required=False,
        label='Nombre',
        widget=forms.TextInput(attrs={
            'placeholder':'tu nombre',
            'class': 'perfil-input'
        })
    )
    last_name=forms.CharField(
        max_length=100,
        required=False,
        label='Apellido',
        widget=forms.TextInput(attrs={
            'placeholder':'Tu apellido',
            'class': 'perfil-input'
        })
    )
    email=forms.EmailField(
        required=True,
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@example.com',
            'class': 'perfil-input'
        })
    )
    edad = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=120,
        label='Edad',
        widget=forms.NumberInput(attrs={
            'class':'perfil-input'
        })
    )
    avatar = forms.ImageField(
        required=False,
        label='Avatar',
        widget=forms.FileInput(attrs={
            'class': 'Perfil-avatar-input',
            'accept': 'image/*'
        })
    )
    preferencias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        label='Categorias favoritas',
        widget=forms.CheckboxSelectMultiple()
    )

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@example.com',
            'class': 'perfil-input'
        })
    )
    class Meta:
        model= User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class ComentarioForm(forms.ModelForm):
    puntuacion = forms.ChoiceField(
        choices=[(i, '⭐' * i) for  i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'puntuacion-radio'}),
        required=False,
        label='Puntuación',
    )

    class Meta:
        model = Comentario
        fields = ['puntuacion', 'titulo', 'mensaje']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Titulo del comentario',
                'class'      : 'comentario-input',
                'maxlength'  : '100'
            }),
            'mensaje': forms.Textarea(attrs={
                'placeholder': 'Cuenta tu experiencia con el servicio...',
                'class': 'comentario-textarea',
                'maxlength': '3000',
                'id': 'comentario-mensaje',
                'rows': 4
            })
        }
        labels = {
            'titulo': 'Título',
            'mensaje': 'Tu comentario',
        }
