from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.training_exercise_item import TrainingExerciseItem
from app.features.training_exercise_items.schemas import TrainingExerciseItemResponse


router = APIRouter()


@router.get("/training-exercise-items", response_model=list[TrainingExerciseItemResponse], status_code=200, tags=["training-exercise-items"])
async def list_training_exercise_items(session: AsyncSession = Depends(get_session)) -> list[TrainingExerciseItemResponse]:

    all_items = await session.execute(
        select(TrainingExerciseItem)
        .options(selectinload(TrainingExerciseItem.body_category))
        .order_by(TrainingExerciseItem.description)
    )
    result = list(all_items.scalars().all())

    return [TrainingExerciseItemResponse.model_validate(item) for item in result]
