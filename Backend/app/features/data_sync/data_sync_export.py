from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.infrastructure.database import get_session
from app.Models.profile import Profile
from app.Models.body_category import BodyCategory
from app.Models.training_exercise_item import TrainingExerciseItem
from app.Models.training_plan import TrainingPlan, TrainingExercise
from app.Models.training_plan_completion import TrainingPlanCompletion
from app.Models.training_exercise_completion import TrainingExerciseCompletion

from app.features.data_sync.schemas import (
    DataSyncExport,
    ProfileSync,
    BodyCategorySync,
    TrainingExerciseItemSync,
    TrainingPlanSync,
    TrainingExerciseSync,
    TrainingPlanCompletionSync,
    TrainingExerciseCompletionSync
)

router = APIRouter(tags=["data-sync"])

@router.get("/data-sync/export", response_model=DataSyncExport)
async def export_data(session: AsyncSession = Depends(get_session)):
    # Fetch all data from all tables
    profiles = (await session.execute(select(Profile))).scalars().all()
    body_categories = (await session.execute(select(BodyCategory))).scalars().all()
    training_exercise_items = (await session.execute(select(TrainingExerciseItem))).scalars().all()
    training_plans = (await session.execute(select(TrainingPlan))).scalars().all()
    training_exercises = (await session.execute(select(TrainingExercise))).scalars().all()
    training_plan_completions = (await session.execute(select(TrainingPlanCompletion))).scalars().all()
    training_exercise_completions = (await session.execute(select(TrainingExerciseCompletion))).scalars().all()

    return DataSyncExport(
        profiles=[ProfileSync.model_validate(p) for p in profiles],
        body_categories=[BodyCategorySync.model_validate(b) for b in body_categories],
        training_exercise_items=[TrainingExerciseItemSync.model_validate(t) for t in training_exercise_items],
        training_plans=[TrainingPlanSync.model_validate(p) for p in training_plans],
        training_exercises=[TrainingExerciseSync.model_validate(e) for e in training_exercises],
        training_plan_completions=[TrainingPlanCompletionSync.model_validate(c) for c in training_plan_completions],
        training_exercise_completions=[TrainingExerciseCompletionSync.model_validate(c) for c in training_exercise_completions]
    )
