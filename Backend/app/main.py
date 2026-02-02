from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.features.health.router import router as health_router
from app.features.profiles import models as profiles_models  # noqa: F401
from app.features.profiles.router import router as profiles_router
from app.infrastructure.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Tabellen anlegen (alle Modelle sind durch Import oben registriert)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Engine schließen
    await engine.dispose()


app = FastAPI(
    title="BearMode API",
    description="Backend mit Vertical Slice Architektur",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "file://", "null"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(profiles_router, prefix="/profiles", tags=["profiles"])