# ---------- 1️⃣ Elige una base ---------- #
# Usa una imagen ligera de Python 3.12
FROM python:3.12-slim

# ---------- 2️⃣ Establece el directorio de trabajo ----------
WORKDIR /app

# ---------- 3️⃣ Copia todo el proyecto ----------
COPY . .

# ---------- 4️⃣ Añade la ruta donde está cuentas.py ----------
ENV PYTHONPATH="/app/output:${PYTHONPATH}"

# ---------- 5️⃣ Instala dependencias ----------
RUN pip install -r requirements.txt

# ---------- 6️⃣ Comando de inicio ----------
# Cambia el script a lo que quieras ejecutar
CMD ["python", "output/app.py"]