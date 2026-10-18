# Analizador de representación de datos

Aplicación web desarrollada con **Python** y **Django** que relaciona los sistemas numéricos y la codificación de caracteres.

## Requisitos

- Python 3.12+
- Django (ver `requirements.txt`)

## Instalación y ejecución (sin Docker)

```powershell
# Clonar el repositorio
git clone <URL-del-repositorio>
cd "Analizador de representacion de datos"

# Crear y activar entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Ejecutar el servidor de desarrollo
python manage.py runserver
```

Luego abre en el navegador: `http://127.0.0.1:8000/`

## Funcionalidades

1. **Conversión de sistemas numéricos**: ingresa un número y selecciona su base de origen (2, 8, 10 o 16). La aplicación valida los dígitos, rango (0 a 65 535) y muestra el resultado en decimal, binario (rellenado al siguiente límite de byte: 8, 16, 24… bits), octal y hexadecimal, además de los bits significativos y bytes necesarios.
2. **Análisis de texto (UTF-8)**: acepta hasta 20 caracteres y muestra, para cada uno: carácter, código decimal, punto de código U+, hexadecimal y sus bytes UTF-8.
3. **Validación**: mensajes claros para entradas vacías, dígitos inválidos, valores negativos y valores fuera de rango.

## Pruebas automatizadas

Ejecutar el conjunto de pruebas:

```powershell
python manage.py test
```

El proyecto incluye pruebas que cubren conversiones válidas, errores de base/rango, negativos, campos vacíos y un caso UTF-8 con la letra `ñ`.

> Nota: esta versión no incluye Docker. Cuando se requiera, se añadirá el `Dockerfile` basado en `python:3.12-slim`, el `compose.yaml` expuesto en el puerto 8000 y los límites de 256 MB RAM / 1 CPU.
