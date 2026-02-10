from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database import Base, engine
from app.features.health.router import router as health_router
from app.features.profiles.router import router as profiles_router
from app.features.training_exercise_items.router import router as training_exercise_items_router
from app.features.training_plan.training_plan_create import router as training_plan_create_router
from app.features.training_plan.training_plan_get_all import router as training_plan_get_all_router
from app.features.training_plan.training_plan_get_by_id import router as training_plan_get_by_id_router
from app.features.training_plan.training_plan_update import router as training_plan_update_router
from app.features.training_plan.training_plan_delete import router as training_plan_delete_router
from app.features.training_plan.training_plan_execute import router as training_plan_execute_router


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
app.include_router(training_exercise_items_router,
                   prefix="/training-exercise-items", tags=["training-exercise-items"])

app.include_router(training_plan_create_router)
app.include_router(training_plan_get_all_router)
app.include_router(training_plan_get_by_id_router)
app.include_router(training_plan_update_router)
app.include_router(training_plan_delete_router)
app.include_router(training_plan_execute_router)
