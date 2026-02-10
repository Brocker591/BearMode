from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.training_plan import TrainingPlan, TrainingExercise
from app.features.training_plan.schemas import TrainingPlanResponse


router = APIRouter()


@router.get("/training-plans/{plan_id}", response_model=TrainingPlanResponse, tags=["training-plans"])
async def get_training_plan(plan_id: UUID, session: AsyncSession = Depends(get_session)) -> TrainingPlanResponse:

    plan = (await session.execute(
        select(TrainingPlan)
        .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
        .where(TrainingPlan.id == plan_id)
    )).scalar_one_or_none()

    if plan is None:
        raise HTTPException(status_code=404, detail="Training Plan not found")

    return TrainingPlanResponse.model_validate(plan)
