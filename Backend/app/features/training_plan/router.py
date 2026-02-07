from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.training_plan.schemas import (
    TrainingPlanCreate,
    TrainingPlanUpdate,
    TrainingPlanResponse,
)
from app.features.training_plan import repository
from app.infrastructure.database import get_session

router = APIRouter()


@router.post("", response_model=TrainingPlanResponse, status_code=201)
async def create_training_plan(
    body: TrainingPlanCreate,
    session: AsyncSession = Depends(get_session)
) -> TrainingPlanResponse:
    plan = await repository.create(
        session, 
        name=body.name, 
        profile_id=body.profile_id, 
        exercises_data=body.training_exercises
    )
    return TrainingPlanResponse.model_validate(plan)


@router.get("", response_model=list[TrainingPlanResponse])
async def list_training_plans(
    session: AsyncSession = Depends(get_session)
) -> list[TrainingPlanResponse]:
    plans = await repository.get_all(session)
    return [TrainingPlanResponse.model_validate(p) for p in plans]


@router.get("/{plan_id}", response_model=TrainingPlanResponse)
async def get_training_plan(
    plan_id: UUID, 
    session: AsyncSession = Depends(get_session)
) -> TrainingPlanResponse:
    plan = await repository.get_by_id(session, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Training Plan not found")
    return TrainingPlanResponse.model_validate(plan)


@router.put("/{plan_id}", response_model=TrainingPlanResponse)
async def update_training_plan(
    plan_id: UUID, 
    body: TrainingPlanUpdate, 
    session: AsyncSession = Depends(get_session)
) -> TrainingPlanResponse:
    plan = await repository.update(
        session, 
        plan_id, 
        name=body.name, 
        profile_id=body.profile_id, 
        exercises_data=body.training_exercises
    )
    if plan is None:
        raise HTTPException(status_code=404, detail="Training Plan not found")
    return TrainingPlanResponse.model_validate(plan)


@router.delete("/{plan_id}", status_code=204)
async def delete_training_plan(
    plan_id: UUID, 
    session: AsyncSession = Depends(get_session)
) -> None:
    deleted = await repository.delete(session, plan_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Training Plan not found")
