from fastapi import APIRouter, Depends
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.training_plan import TrainingPlan, TrainingExercise
from app.features.training_plan.schemas import TrainingPlanResponse


router = APIRouter()


@router.get("/training-plans", response_model=list[TrainingPlanResponse], status_code=200, tags=["training-plans"])
async def list_training_plans(session: AsyncSession = Depends(get_session)) -> list[TrainingPlanResponse]:

    all_plans = await session.execute(
        select(TrainingPlan)
        .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
        .order_by(TrainingPlan.name)
    )
    result = list(all_plans.scalars().all())

    return [TrainingPlanResponse.model_validate(plan) for plan in result]
