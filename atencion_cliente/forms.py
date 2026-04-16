from django import forms
from .models import Comentario

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