from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.training_exercise_item import TrainingExerciseItem
from app.features.training_exercise_items.schemas import TrainingExerciseItemUpdate, TrainingExerciseItemResponse


router = APIRouter()


@router.put("/training-exercise-items/{item_id}", response_model=TrainingExerciseItemResponse, tags=["training-exercise-items"])
async def update_training_exercise_item(item_id: UUID, body: TrainingExerciseItemUpdate, session: AsyncSession = Depends(get_session)) -> TrainingExerciseItemResponse:
    
    item = (await session.execute(
        select(TrainingExerciseItem)
        .where(TrainingExerciseItem.id == item_id)
    )).scalar_one_or_none()

    if item is None:
        raise HTTPException(
            status_code=404, detail="Training exercise item not found")

    # Check for duplicate description
    existing_description = (await session.execute(
        select(TrainingExerciseItem)
        .where(TrainingExerciseItem.description == body.description)
        .where(TrainingExerciseItem.id != item_id)
    )).scalar_one_or_none()

    if existing_description is not None:
        raise HTTPException(status_code=409, detail="Description already exists")

    item.description = body.description
    item.video_url = body.video_url
    item.body_category_id = body.body_category_id
    
    await session.flush()
    # Eager load the relationship for the response
    item = (await session.execute(
        select(TrainingExerciseItem)
        .options(selectinload(TrainingExerciseItem.body_category))
        .where(TrainingExerciseItem.id == item.id)
    )).scalar_one()

    return TrainingExerciseItemResponse.model_validate(item)
