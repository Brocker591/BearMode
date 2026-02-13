from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.features.excersice_completion.schemas import TrainingExerciseCompletion
from app.Models.training_exercise_completion import TrainingExerciseCompletion as TrainingExerciseCompletionModel

router = APIRouter()


@router.get("/exercice-completion/byProfileId/{profile_id}", response_model=list[TrainingExerciseCompletion], status_code=200, tags=["exercice-completion"])
async def list_training_plans(profile_id: str, session: AsyncSession = Depends(get_session)) -> list[TrainingExerciseCompletion]:

    all_plans = await session.execute(
        select(TrainingExerciseCompletionModel)
        .where(TrainingExerciseCompletionModel.profile_id == profile_id)
        .order_by(TrainingExerciseCompletionModel.training_day.desc())
        .order_by(TrainingExerciseCompletionModel.training_plan_id.desc())
        .order_by(TrainingExerciseCompletionModel.order)
    )
    result = list(all_plans.scalars().all())

    return [TrainingExerciseCompletion.model_validate(plan) for plan in result]
