from django import forms

class CheckoutForm(forms.Form):
    nombre_titular = forms.CharField(
        max_length=100,
        label='Nombre del titular',
        widget=forms.TextInput(attrs={
            'placeholder': 'Como figura en la tarjeta',
            'class': 'checkout-input',
            'autocomplete': 'cc-name'
        })
    )
    numero_tarjeta = forms.CharField(
        max_length=19,
        label='Número de tarjeta',
        widget=forms.TextInput(attrs={
            'placeholder': '1234 5678 9012 3456',
            'class': 'checkout-input',
            'autocomplete': 'cc-number',
            'maxlength': '19',
            'id': 'numero-tarjeta'
        })
    )
    vencimiento = forms.CharField(
        max_length=5,
        label='Vencimiento',
        widget=forms.TextInput(attrs={
            'placeholder': 'MM/AA',
            'class': 'checkout-input-boxes checkout-input-sm',
            'autocomplete': 'cc-exp',
            'max-length': '5',
            'id': 'vencimiento'
        })
    )
    cvv = forms.CharField(
        max_length = 4,
        label='CVV',
        widget=forms.TextInput(attrs={
            'placeholder': '123',
            'class': 'checkout-input-boxes checkout-input-sm',
            'autocomplete': 'cc-csc',
            'maxlength': '4',
            'id': 'cvv',
            'type': 'password'
        })
    )
    def clean_numero_tarjeta(self):
        numero = self.cleaned_data.get('numero_tarjeta', '')
        solo_digitos = numero.replace(' ', '')
        if not solo_digitos.isdigit():
            raise forms.ValidationError('El número de la tarjeta sólo puede contener dígitos.')
        if len(solo_digitos) != 16:
            raise forms.ValidationError('El número de tarjeta debe tener 16 dígitos.')
        return numero
    
    def clean_vencimiento(self):
        venc = self.cleaned_data.get('vencimiento', '')
        if len(venc) != 5 or venc[2] != '/':
            raise forms.ValidationError('Formato inválido. Usa MM/AA')
        mes, anio = venc.split('/')
        if not mes.isdigit() or not anio.isdigit():
            raise forms.ValidationError('Formato inválido. Usa MM/AA.')
        if int(mes) < 1 or int(mes) > 12:
            return forms.ValidationError('El mes debe estar entre 01 y 12.')
        return venc
    
    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv', '')
        if not cvv.isdigit():
            raise forms.ValidationError('El CVV solo puede contener dígitos.')
        if len(cvv) not in [3, 4]:
            raise forms.ValidationError('El CVV debe tener 3 o 4 dígitos.')
        return cvv