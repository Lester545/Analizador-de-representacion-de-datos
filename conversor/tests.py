from django.test import SimpleTestCase

from conversor.forms import ConversionForm, TextoForm
from conversor.views import analizar_caracter, convertir_resultado


class ConversionValidaTests(SimpleTestCase):
    """Pruebas de conversiones válidas entre sistemas numéricos."""

    def test_binario_a_decimal_y_representaciones(self):
        resultado = convertir_resultado(int('1010', 2))
        self.assertEqual(resultado['decimal'], 10)
        self.assertEqual(resultado['binario'], '00001010')  # relleno a 8 bits
        self.assertEqual(resultado['octal'], '12')
        self.assertEqual(resultado['hexadecimal'], 'A')
        self.assertEqual(resultado['bits_significativos'], 4)
        self.assertEqual(resultado['bytes_necesarios'], 1)

    def test_hexadecimal_ff(self):
        resultado = convertir_resultado(int('FF', 16))
        self.assertEqual(resultado['decimal'], 255)
        self.assertEqual(resultado['binario'], '11111111')
        self.assertEqual(resultado['hexadecimal'], 'FF')
        self.assertEqual(resultado['bytes_necesarios'], 1)

    def test_valor_limite_65535_ocupa_dos_bytes(self):
        resultado = convertir_resultado(65535)
        self.assertEqual(resultado['decimal'], 65535)
        self.assertEqual(resultado['binario'], '1111111111111111')  # 16 bits
        self.assertEqual(resultado['bits_significativos'], 16)
        self.assertEqual(resultado['bytes_necesarios'], 2)

    def test_cero(self):
        resultado = convertir_resultado(0)
        self.assertEqual(resultado['decimal'], 0)
        self.assertEqual(resultado['binario'], '00000000')
        self.assertEqual(resultado['bits_significativos'], 0)
        self.assertEqual(resultado['bytes_necesarios'], 1)


class ValidacionFormularioTests(SimpleTestCase):
    """Pruebas de validación: base, rango y negativos."""

    def test_digitos_invalidos_para_base_binaria(self):
        form = ConversionForm(data={'numero': '102', 'base': '2'})
        self.assertFalse(form.is_valid())
        self.assertIn('inválidos para la base 2', str(form.errors['numero']))

    def test_valor_fuera_de_rango(self):
        form = ConversionForm(data={'numero': '65536', 'base': '10'})
        self.assertFalse(form.is_valid())
        self.assertIn('0 y 65535', str(form.errors['numero']))

    def test_valor_negativo_rechazado(self):
        form = ConversionForm(data={'numero': '-5', 'base': '10'})
        self.assertFalse(form.is_valid())
        self.assertIn('negativos', str(form.errors['numero']))

    def test_campo_vacio(self):
        form = ConversionForm(data={'numero': '', 'base': '10'})
        self.assertFalse(form.is_valid())
        self.assertIn('required', str(form.errors['numero']).lower())

    def test_texto_con_enie_utf8(self):
        analisis = analizar_caracter('ñ')
        self.assertEqual(analisis['caracter'], 'ñ')
        self.assertEqual(analisis['decimal'], 241)
        self.assertEqual(analisis['punto_unicode'], 'U+00F1')
        self.assertEqual(analisis['hex'], 'F1')
        self.assertEqual(analisis['bytes_utf8'], 'C3 B1')

    def test_formulario_texto_acepta_hasta_20_caracteres(self):
        form = TextoForm(data={'texto': 'a' * 20})
        self.assertTrue(form.is_valid())

    def test_formulario_texto_rechaza_mas_de_20(self):
        form = TextoForm(data={'texto': 'a' * 21})
        self.assertFalse(form.is_valid())
