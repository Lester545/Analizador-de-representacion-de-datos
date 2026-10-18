from django.shortcuts import render

from .forms import ConversionForm, TextoForm

MIN_VALOR = 0
MAX_VALOR = 65535


def _rellenar_a_limite_de_byte(binario_plano: str, bits: int) -> str:
    """Rellena con ceros a la izquierda hasta el siguiente límite de byte (8, 16, 24... bits)."""
    if bits == 0:
        return '0' * 8
    limite = ((bits + 7) // 8) * 8
    return binario_plano.zfill(limite)


def convertir_resultado(decimal: int) -> dict:
    """Devuelve un diccionario con las representaciones del número decimal."""
    bits_significativos = decimal.bit_length()
    binario_plano = bin(decimal)[2:]  # quita el prefijo '0b'
    binario = _rellenar_a_limite_de_byte(binario_plano, bits_significativos)
    octal = oct(decimal)[2:]  # quita el prefijo '0o'
    hexadecimal = hex(decimal)[2:].upper()  # quita el prefijo '0x'
    bytes_necesarios = (bits_significativos + 7) // 8 or 1

    return {
        'decimal': decimal,
        'binario': binario,
        'octal': octal,
        'hexadecimal': hexadecimal,
        'bits_significativos': bits_significativos,
        'bytes_necesarios': bytes_necesarios,
    }


def analizar_caracter(car: str) -> dict:
    """Devuelve el análisis de un solo carácter: código, punto U+, hex y bytes UTF-8."""
    codigo_decimal = ord(car)
    bytes_utf8 = car.encode('utf-8')
    return {
        'caracter': car,
        'decimal': codigo_decimal,
        'punto_unicode': f'U+{codigo_decimal:04X}',
        'hex': f'{codigo_decimal:X}',
        'bytes_utf8': ' '.join(f'{byte:02X}' for byte in bytes_utf8),
        'num_bytes': len(bytes_utf8),
    }


def index(request):
    form_num = None
    form_txt = None
    resultado_num = None
    analisis_texto = None

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'numerico':
            form_num = ConversionForm(request.POST)
            if form_num.is_valid():
                decimal = form_num.cleaned_data['decimal']
                resultado_num = convertir_resultado(decimal)
                resultado_num['numero_original'] = form_num.cleaned_data['numero']
                resultado_num['base_origen'] = int(form_num.cleaned_data['base'])
        elif accion == 'texto':
            form_txt = TextoForm(request.POST)
            if form_txt.is_valid():
                texto = form_txt.cleaned_data['texto']
                analisis_texto = [analizar_caracter(c) for c in texto]

    if form_num is None:
        form_num = ConversionForm()
    if form_txt is None:
        form_txt = TextoForm()

    return render(request, 'conversor/index.html', {
        'form_num': form_num,
        'form_txt': form_txt,
        'resultado_num': resultado_num,
        'analisis_texto': analisis_texto,
    })
