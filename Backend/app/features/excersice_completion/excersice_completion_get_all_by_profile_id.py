from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.training_plan import TrainingPlan, TrainingExercise
from app.features.training_plan.schemas import TrainingExerciseCompletion
from app.Models.training_exercise_completion import TrainingExerciseCompletion as TrainingExerciseCompletionModel

router = APIRouter()


@router.get("/training-plans/byProfileId/{profile_id}", response_model=list[TrainingExerciseCompletion], status_code=200, tags=["training-plans"])
async def list_training_plans(profile_id: str, session: AsyncSession = Depends(get_session)) -> list[TrainingExerciseCompletion]:

    all_plans = await session.execute(
        select(TrainingExerciseCompletionModel)
        .where(TrainingExerciseCompletionModel.profile_id == profile_id)
        .order_by(TrainingExerciseCompletionModel.created_on.desc())
        .order_by(TrainingExerciseCompletionModel.order)
    )
    result = list(all_plans.scalars().all())

    return [TrainingExerciseCompletion.model_validate(plan) for plan in result]
