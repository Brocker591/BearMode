# BearMode - Gemini Project Context

## Project Overview
BearMode is a full-stack workout and fitness tracking application. It features a robust FastAPI backend and a modern Angular frontend, which can also be run as a desktop application using Electron.

- **Backend:** FastAPI (Python 3.11+) with Vertical Slice Architecture.
- **Frontend:** Angular 21 with Material Design, Tailwind CSS 4, and Electron for desktop builds.
- **Database:** PostgreSQL with SQLAlchemy (Asyncpg).
- **Deployment:** Supports Docker, Local execution, and AppImage for desktop.

## Project Structure
- `Backend/`: FastAPI application.
    - `app/features/`: Contains vertical slices for each feature (e.g., `profiles`, `training_plan`).
    - `app/infrastructure/`: Database connection and initialization.
    - `app/Models/`: SQLAlchemy models.
- `Frontend/bearmode/`: Angular application.
    - `src/app/pages/`: Feature-specific pages.
    - `src/app/services/`: API interaction services.
    - `electron/`: Electron main process and configuration.
- `docker-compose.yml`: Local development services (PostgreSQL).

## Building and Running

### Backend
1. **Setup Environment:**
   ```bash
   cd Backend
   python -m venv .venv
   source .venv/bin/activate # Linux/macOS
   # .venv\Scripts\Activate.ps1 # Windows
   pip install -r requirements.txt
   ```
2. **Environment Variables:**
   - Copy `.env.example` to `.env`.
   - Update `DATABASE_URL` as needed (defaults to `postgresql+asyncpg://postgres:postgres@localhost:5432/bearmode`).
3. **Run API:**
   ```bash
   uvicorn app.main:app --reload
   ```
   - API Docs: `http://localhost:8000/docs`

### Frontend
1. **Setup:**
   ```bash
   cd Frontend/bearmode
   npm install
   ```
2. **Run Web:**
   ```bash
   npm start
   ```
   - URL: `http://localhost:4200`
3. **Run Electron (Dev):**
   ```bash
   npm run electron:dev
   ```
4. **Build Electron (AppImage):**
   ```bash
   npm run build:electron
   ```

### Docker
Run `docker-compose up -d` to start the PostgreSQL database.

## Development Conventions

### Backend (Vertical Slice Architecture)
- Each feature is self-contained in `app/features/<feature_name>/`.
- A feature typically includes:
    - `router.py` (or specific operation files like `profile_create.py`).
    - `schemas.py` (Pydantic models).
    - `repository.py` (optional, for DB logic).
- Register new routers in `app/main.py`.
- Use async database operations exclusively.

### Frontend
- **Framework:** Angular 21 (standalone components).
- **Styling:** Tailwind CSS 4 and Angular Material.
- **State Management:** Services with RxJS.
- **Formatting:** Prettier is configured in `package.json`.
- **Charts:** Chart.js with `ng2-charts`.

### Testing
- **Backend:** Manual verification scripts are located in the root of the `Backend/` directory (e.g., `verify_profile_deletion.py`).
- **Frontend:** Vitest for unit tests (`npm test`).

## Key Files
- `Backend/app/main.py`: FastAPI entry point and middleware.
- `Backend/app/config.py`: Configuration and environment variable loading.
- `Frontend/bearmode/src/app/app.routes.ts`: Frontend routing configuration.
- `Frontend/bearmode/electron/main.js`: Electron entry point.
- `GEMINI.md`: This file (instructional context).
