from django import forms

BASE_CHOICES = [
    ('2', 'Binario (base 2)'),
    ('8', 'Octal (base 8)'),
    ('10', 'Decimal (base 10)'),
    ('16', 'Hexadecimal (base 16)'),
]

DIGITOS_POR_BASE = {
    '2': set('01'),
    '8': set('01234567'),
    '10': set('0123456789'),
    '16': set('0123456789ABCDEFabcdef'),
}

MIN_VALOR = 0
MAX_VALOR = 65535


class ConversionForm(forms.Form):
    """Formulario para convertir un número de una base a decimal/binario/octal/hex."""

    numero = forms.CharField(
        label='Número',
        max_length=50,
        strip=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej. 1010',
            'autocomplete': 'off',
        }),
    )
    base = forms.ChoiceField(
        label='Base de origen',
        choices=BASE_CHOICES,
    )

    def clean_numero(self):
        valor = self.cleaned_data.get('numero', '')
        if not valor:
            raise forms.ValidationError('Ingrese un número.')
        if valor.startswith('-'):
            raise forms.ValidationError('No se permiten valores negativos.')
        return valor

    def clean(self):
        cleaned = super().clean()
        numero = cleaned.get('numero', '')
        base_sel = cleaned.get('base')

        if not numero or not base_sel:
            return cleaned

        base = int(base_sel)
        validos = DIGITOS_POR_BASE[base_sel]

        if not all(c.upper() in validos for c in numero):
            self.add_error('numero', f'Dígitos inválidos para la base {base}.')
            return cleaned

        try:
            decimal = int(numero, base)
        except ValueError:
            self.add_error('numero', f'Dígitos inválidos para la base {base}.')
            return cleaned

        if decimal < MIN_VALOR or decimal > MAX_VALOR:
            self.add_error(
                'numero',
                f'El valor debe estar entre {MIN_VALOR} y {MAX_VALOR}.',
            )
            return cleaned

        cleaned['decimal'] = decimal
        return cleaned


class TextoForm(forms.Form):
    """Formulario para analizar los caracteres y su codificación UTF-8 de un texto."""

    texto = forms.CharField(
        label='Texto',
        max_length=20,
        strip=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Hasta 20 caracteres',
            'autocomplete': 'off',
        }),
    )

    def clean_texto(self):
        valor = self.cleaned_data.get('texto', '')
        if not valor:
            raise forms.ValidationError('Ingrese un texto.')
        if len(valor) > 20:
            raise forms.ValidationError('El texto no puede exceder los 20 caracteres.')
        return valor
