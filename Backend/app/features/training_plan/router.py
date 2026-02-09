from math import e
from uuid import UUID
from venv import create

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.training_plan.schemas import (
    TrainingExerciseResponse,
    TrainingPlanCreate,
    TrainingPlanUpdate,
    TrainingPlanResponse,
    TrainingExerciseItemResponse
)
import app.features.training_plan.repository as repository
from app.infrastructure.database import get_session

router = APIRouter()


@router.post("", response_model=TrainingPlanResponse, status_code=201)
async def create_training_plan(body: TrainingPlanCreate, session: AsyncSession = Depends(get_session)) -> TrainingPlanResponse:
    try:
        plan = await repository.create(session, training_plan=body)
        return TrainingPlanResponse.model_validate(plan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=list[TrainingPlanResponse], status_code=200)
async def list_training_plans(session: AsyncSession = Depends(get_session)) -> list[TrainingPlanResponse]:
    plans = await repository.get_all(session)
    return [TrainingPlanResponse.model_validate(plan) for plan in plans]


@router.get("/{plan_id}", response_model=TrainingPlanResponse)
async def get_training_plan(
    plan_id: UUID,
    session: AsyncSession = Depends(get_session)
) -> TrainingPlanResponse:
    plan = await repository.get_by_id(session, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Training Plan not found")
    return TrainingPlanResponse.model_validate(plan)


@router.put("", response_model=TrainingPlanResponse)
async def update_training_plan(body: TrainingPlanUpdate, session: AsyncSession = Depends(get_session)) -> TrainingPlanResponse:
    try:
        plan = await repository.update(session, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
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
