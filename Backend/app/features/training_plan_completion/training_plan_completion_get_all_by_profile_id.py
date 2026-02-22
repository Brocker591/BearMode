from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.features.training_plan_completion.schemas import TrainingPlanCompletion
from app.Models.training_plan_completion import TrainingPlanCompletion as TrainingPlanCompletionModel

router = APIRouter()

@router.get("/training-plan-completion/byProfileId/{profile_id}", response_model=list[TrainingPlanCompletion], status_code=200, tags=["training-plan-completion"])
async def list_training_plan_completions(profile_id: str, session: AsyncSession = Depends(get_session)) -> list[TrainingPlanCompletion]:

    all_completions = await session.execute(
        select(TrainingPlanCompletionModel)
        .where(TrainingPlanCompletionModel.profile_id == profile_id)
        .order_by(TrainingPlanCompletionModel.training_day.desc())
        .order_by(TrainingPlanCompletionModel.created_at.desc())
    )
    result = list(all_completions.scalars().all())

    return [TrainingPlanCompletion.model_validate(comp) for comp in result]
