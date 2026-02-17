from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
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

    item = TrainingExerciseItem(description=body.description, video_url=body.video_url)
    session.add(item)
    await session.flush()
    await session.refresh(item)

    return TrainingExerciseItemResponse.model_validate(item)
