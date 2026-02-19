from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database import Base, engine, get_session
from app.infrastructure.initial_data import init_db
from app.features.health.router import router as health_router
from app.features.profiles.profile_create import router as profile_create_router
from app.features.profiles.profile_get_all import router as profile_get_all_router
from app.features.profiles.profile_get_by_id import router as profile_get_by_id_router
from app.features.profiles.profile_update import router as profile_update_router
from app.features.profiles.profile_delete import router as profile_delete_router
from app.features.training_exercise_items.training_exercise_item_create import router as training_exercise_item_create_router
from app.features.training_exercise_items.training_exercise_item_get_all import router as training_exercise_item_get_all_router
from app.features.training_exercise_items.training_exercise_item_get_by_id import router as training_exercise_item_get_by_id_router
from app.features.training_exercise_items.training_exercise_item_update import router as training_exercise_item_update_router
from app.features.training_exercise_items.training_exercise_item_delete import router as training_exercise_item_delete_router
from app.features.training_plan.training_plan_create import router as training_plan_create_router
from app.features.training_plan.training_plan_get_all import router as training_plan_get_all_router
from app.features.training_plan.training_plan_get_all_by_profile_id import router as training_plan_get_all_by_profile_id_router
from app.features.training_plan.training_plan_get_by_id import router as training_plan_get_by_id_router
from app.features.training_plan.training_plan_update import router as training_plan_update_router
from app.features.training_plan.training_plan_delete import router as training_plan_delete_router
from app.features.training_plan.training_plan_execute import router as training_plan_execute_router
from app.features.excersice_completion.excersice_completion_create import router as training_plan_completion_router
from app.features.excersice_completion.excersice_completion_get_all_by_profile_id import router as excersice_completion_get_all_by_profile_id_router
from app.features.body_category.body_category_create import router as body_category_create_router
from app.features.body_category.body_category_get_all import router as body_category_get_all_router
from app.features.body_category.body_category_get_by_id import router as body_category_get_by_id_router
from app.features.body_category.body_category_update import router as body_category_update_router
from app.features.body_category.body_category_delete import router as body_category_delete_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Tabellen anlegen (alle Modelle sind durch Import oben registriert)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Init Data
    async for session in get_session():
        await init_db(session)
        break
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
app.include_router(profile_create_router)
app.include_router(profile_get_all_router)
app.include_router(profile_get_by_id_router)
app.include_router(profile_update_router)
app.include_router(profile_delete_router)
app.include_router(training_exercise_item_create_router)
app.include_router(training_exercise_item_get_all_router)
app.include_router(training_exercise_item_get_by_id_router)
app.include_router(training_exercise_item_update_router)
app.include_router(training_exercise_item_delete_router)
app.include_router(training_plan_create_router)
app.include_router(training_plan_get_all_router)
app.include_router(training_plan_get_all_by_profile_id_router)
app.include_router(training_plan_get_by_id_router)
app.include_router(training_plan_update_router)
app.include_router(training_plan_delete_router)
app.include_router(training_plan_execute_router)
app.include_router(excersice_completion_get_all_by_profile_id_router)

app.include_router(training_plan_completion_router)
app.include_router(body_category_create_router)
app.include_router(body_category_get_all_router)
app.include_router(body_category_get_by_id_router)
app.include_router(body_category_update_router)
app.include_router(body_category_delete_router)