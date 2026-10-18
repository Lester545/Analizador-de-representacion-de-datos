FROM python:3.12-slim

WORKDIR /app

# Evita que Python genere archivos .pyc y que bufere la salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el proyecto
COPY . .

# Expone el puerto de Django
EXPOSE 8000

# Aplica migraciones y levanta el servidor de desarrollo accesible desde el contenedor
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
