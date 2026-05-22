# Usar una imagen base de Python oficial, ligera y optimizada para producción
FROM python:3.11-slim

# Evitar la escritura de archivos .pyc y asegurar salida de consola fluida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema mínimas necesarias (como curl)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos primero para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instalar las dependencias de Python usando wheels precompilados para Linux x86_64
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto al contenedor
COPY . .

# Crear la carpeta data si no existe para almacenamiento local de respaldo
RUN mkdir -p data

# Comando para arrancar el servidor usando el script de inicialización del proyecto
# Railway inyecta dinámicamente el puerto mediante la variable PORT y redirige el tráfico
# automáticamente al puerto en el que el servidor web se enlaza en tiempo de ejecución.
CMD ["python", "main.py"]
