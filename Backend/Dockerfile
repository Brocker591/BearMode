# Verwende ein offizielles Python-Laufzeit-Image als Basis
FROM python:3.11-slim

# Verhindere, dass Python pyc-Dateien auf die Festplatte schreibt
ENV PYTHONDONTWRITEBYTECODE 1
# Verhindere, dass Python stdout und stderr puffert
ENV PYTHONUNBUFFERED 1

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere Systemabhängigkeiten, falls für einige Python-Pakete (z.B. in Verbindung mit DB) eine Kompilierung nötig ist
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Kopiere die Abhängigkeiten-Datei in das Arbeitsverzeichnis
COPY requirements.txt .

# Installiere die benötigten Pakete
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten restlichen Quellcode in das Arbeitsverzeichnis
COPY . .

# Teile Docker mit, dass der Container auf Port 8000 lauscht
EXPOSE 8000

# Definiere den Befehl zum Ausführen der Anwendung
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
