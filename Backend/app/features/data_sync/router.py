import json
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

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

@router.post("/data-sync/import")
async def import_data(data: DataSyncExport, session: AsyncSession = Depends(get_session)):
    # 1. Delete all existing data in reverse dependency order
    await session.execute(delete(TrainingExerciseCompletion))
    await session.execute(delete(TrainingPlanCompletion))
    await session.execute(delete(TrainingExercise))
    await session.execute(delete(TrainingPlan))
    await session.execute(delete(TrainingExerciseItem))
    await session.execute(delete(BodyCategory))
    await session.execute(delete(Profile))
    
    # 2. Insert new data in dependency order
    for p in data.profiles:
        session.add(Profile(**p.model_dump()))
    await session.flush()
    
    for b in data.body_categories:
        session.add(BodyCategory(**b.model_dump()))
    await session.flush()
        
    for tp in data.training_plans:
        session.add(TrainingPlan(**tp.model_dump()))
    await session.flush()
        
    for t in data.training_exercise_items:
        session.add(TrainingExerciseItem(**t.model_dump()))
    await session.flush()
        
    for te in data.training_exercises:
        session.add(TrainingExercise(**te.model_dump()))
    await session.flush()
        
    for tpc in data.training_plan_completions:
        session.add(TrainingPlanCompletion(**tpc.model_dump()))
    await session.flush()
        
    for tec in data.training_exercise_completions:
        session.add(TrainingExerciseCompletion(**tec.model_dump()))
    await session.flush()
        
    await session.commit()
    
    return {"message": "Data imported successfully."}
