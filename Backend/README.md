# BearMode Backend

FastAPI-Projekt mit **Vertical Slice Architektur** und PostgreSQL-Anbindung. Läuft lokal unter **Windows** und **Linux**.

## Voraussetzungen

- Python 3.11+
- PostgreSQL (lokal oder per Docker)

## Setup (Windows / Linux)

### 1. Virtuelle Umgebung

```bash
cd Backend
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 2. Abhängigkeiten

```bash
pip install -r requirements.txt
```

### 3. Umgebungsvariablen

`.env` aus der Vorlage anlegen und anpassen:

```bash
cp .env.example .env
```

In `.env` die `DATABASE_URL` auf deine PostgreSQL-Instanz setzen, z. B.:

- Lokal: `postgresql+asyncpg://postgres:postgres@localhost:5432/bearmode`
- Docker: Host je nach Setup z. B. `host.docker.internal` (Windows/Mac) oder der Service-Name `postgres` in docker-compose

### 4. Datenbank

PostgreSQL starten (lokal installiert oder z. B. Docker):

```bash
# Beispiel: PostgreSQL-Container
docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=bearmode -p 5432:5432 postgres:16
```

Die Datenbank muss existieren; Tabellen legst du bei Bedarf per SQL oder über deine Anwendung an.

### 5. API starten

Aus dem Ordner `Backend`:

```bash
uvicorn app.main:app --reload
```

- API: <http://127.0.0.1:8000>
- OpenAPI: <http://127.0.0.1:8000/docs>
- Health-Check: <http://127.0.0.1:8000/health>

## Projektstruktur (Vertical Slices)

- `app/main.py` – FastAPI-App, Lifespan, Router-Einbindung
- `app/config.py` – Einstellungen (z. B. `DATABASE_URL`)
- `app/infrastructure/database.py` – Async-Engine, Session, `get_session`
- `app/features/<name>/` – je ein Slice (z. B. `health`): `router.py`, `schemas.py`, ggf. `repository.py`

Neue Features als neuer Ordner unter `app/features/` anlegen und den Router in `main.py` einbinden.
