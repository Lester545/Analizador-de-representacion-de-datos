# Analizador de representación de datos

Aplicación web desarrollada con **Python 3.12** y **Django** que relaciona los sistemas numéricos y la codificación de caracteres.

## Requisitos

- Python 3.12+
- Django (ver `requirements.txt`)
- Docker y Docker Compose (opcional, para ejecución en contenedor)

---

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

---

## Ejecución con Docker

### Construir y ejecutar la aplicación

Desde la carpeta raíz del proyecto:

```powershell
# Construir la imagen y levantar el contenedor
docker compose up --build

# Ejecutar en segundo plano (desaparecido)
docker compose up --build -d

# Detener y eliminar contenedores
docker compose down
```

La aplicación quedará disponible en: `http://localhost:8000/`

### Límites de recursos aplicados

El `compose.yaml` limita el contenedor a:

- **1 CPU**
- **256 MB de RAM**

Puedes verificar el consumo con:

```powershell
docker stats
```

---

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

---

## Explicación técnica

### Recursos de la arquitectura de Von Neumann que usa la aplicación

La aplicación web utiliza los cinco componentes clásicos de la arquitectura de Von Neumann:

1. **Memoria**: almacena el código de Django, las definiciones de modelos, formularios, vistas y plantillas, así como los datos temporales de los números y textos ingresados por el usuario. La base de datos SQLite (`db.sqlite3`) guarda información persistente en disco.
2. **Unidad de Procesamiento (CPU)**: ejecuta las instrucciones de Python y Django: valida las entradas, realiza las conversiones entre bases numéricas, calcula bits significativos y bytes, y codifica caracteres a UTF-8.
3. **Entrada**: el usuario introduce datos a través de los formularios web (número, base, texto) enviados por HTTP.
4. **Salida**: el servidor devuelve las páginas HTML con los resultados de conversión y análisis al navegador del usuario.
5. **Interconexión (bus)**: la comunicación interna entre la CPU, la memoria y los componentes de E/S dentro del servidor Django.

### ¿Por qué el contenedor comparte el kernel del host?

Los contenedores de Docker **no son máquinas virtuales**. No emulan hardware completo ni incluyen un sistema operativo invitado independiente. En su lugar, utilizan:

- **Namespaces**: aíslan procesos, red, montajes, usuarios y nombres de host.
- **Cgroups**: limitan y aíslan el uso de recursos (CPU, memoria, E/S).

Gracias a esto, el contenedor **comparte el núcleo (kernel) del sistema operativo host**. Esto hace que los contenedores sean mucho más ligeros y rápidos de iniciar que una máquina virtual, ya que no necesitan arrancar un sistema operativo completo ni virtualizar la CPU. Solo empaquetan la aplicación y sus dependencias (Python 3.12, Django, librerías), corriendo sobre el mismo kernel que el equipo donde se ejecuta Docker Desktop.
