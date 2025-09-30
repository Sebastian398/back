FROM python:3.11-slim

# Evitar buffering para logs en consola en tiempo real
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2 y compilación
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copiar y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el backend
COPY . .

EXPOSE 8000

# Arrancar servidor con gunicorn (ajusta nombre de tu proyecto)
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
