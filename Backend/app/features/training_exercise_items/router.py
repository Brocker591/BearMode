from math import e
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.shared.repository import TrainingExerciseItemRepository
from app.features.training_exercise_items.schemas import (
    TrainingExerciseItemCreate,
    TrainingExerciseItemUpdate,
    TrainingExerciseItemResponse
)

router = APIRouter()


@router.post("", response_model=TrainingExerciseItemResponse, status_code=201)
async def create_training_exercise_item(
    body: TrainingExerciseItemCreate,
    session: AsyncSession = Depends(get_session)
) -> TrainingExerciseItemResponse:
    existing = await TrainingExerciseItemRepository.get_by_description(session, body.description)
    if existing is not None:
        raise HTTPException(
            status_code=409, detail="Description already exists")
    item = await TrainingExerciseItemRepository.create(session, body.description, body.video_url)
    return TrainingExerciseItemResponse.model_validate(item)


@router.get("", response_model=list[TrainingExerciseItemResponse])
async def list_training_exercise_items(session: AsyncSession = Depends(get_session)) -> list[TrainingExerciseItemResponse]:
    items = await TrainingExerciseItemRepository.get_all(session)
    return [TrainingExerciseItemResponse.model_validate(i) for i in items]


@router.get("/{item_id}", response_model=TrainingExerciseItemResponse)
async def get_training_exercise_item(item_id: UUID, session: AsyncSession = Depends(get_session)) -> TrainingExerciseItemResponse:
    item = await TrainingExerciseItemRepository.get_by_id(session, item_id)
    if item is None:
        raise HTTPException(
            status_code=404, detail="Training exercise item not found")
    return TrainingExerciseItemResponse.model_validate(item)


@router.put("/{item_id}", response_model=TrainingExerciseItemResponse)
async def update_training_exercise_item(item_id: UUID, body: TrainingExerciseItemUpdate, session: AsyncSession = Depends(get_session)) -> TrainingExerciseItemResponse:
    item = await TrainingExerciseItemRepository.update(session, item_id, body.description, body.video_url)
    if item is None:
        raise HTTPException(
            status_code=404, detail="Training exercise item not found")
    return TrainingExerciseItemResponse.model_validate(item)


@router.delete("/{item_id}", status_code=204)
async def delete_training_exercise_item(item_id: UUID, session: AsyncSession = Depends(get_session)) -> None:
    deleted = await TrainingExerciseItemRepository.delete(session, item_id)
    if not deleted:
        raise HTTPException(
            status_code=404, detail="Training exercise item not found")
