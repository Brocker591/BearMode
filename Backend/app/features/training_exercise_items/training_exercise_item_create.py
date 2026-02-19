from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.training_exercise_item import TrainingExerciseItem
from app.features.training_exercise_items.schemas import TrainingExerciseItemCreate, TrainingExerciseItemResponse


router = APIRouter()


@router.post("/training-exercise-items", response_model=TrainingExerciseItemResponse, status_code=201, tags=["training-exercise-items"])
async def create_training_exercise_item(body: TrainingExerciseItemCreate, session: AsyncSession = Depends(get_session)) -> TrainingExerciseItemResponse:
    
    existing = (await session.execute(
        select(TrainingExerciseItem)
        .where(TrainingExerciseItem.description == body.description)
    )).scalar_one_or_none()

    if existing is not None:
        raise HTTPException(
            status_code=409, detail="Description already exists")

    item = TrainingExerciseItem(
        description=body.description,
        video_url=body.video_url,
        body_category_id=body.body_category_id
    )
    session.add(item)
    await session.flush()
    # Eager load the relationship for the response
    item = (await session.execute(
        select(TrainingExerciseItem)
        .options(selectinload(TrainingExerciseItem.body_category))
        .where(TrainingExerciseItem.id == item.id)
    )).scalar_one()

    return TrainingExerciseItemResponse.model_validate(item)
