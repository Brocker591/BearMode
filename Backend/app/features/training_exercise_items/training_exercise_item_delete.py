from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.training_exercise_item import TrainingExerciseItem


router = APIRouter()


@router.delete("/training-exercise-items/{item_id}", status_code=204, tags=["training-exercise-items"])
async def delete_training_exercise_item(item_id: UUID, session: AsyncSession = Depends(get_session)) -> None:

    item = (await session.execute(
        select(TrainingExerciseItem)
        .where(TrainingExerciseItem.id == item_id)
    )).scalar_one_or_none()

    if item is None:
        raise HTTPException(
            status_code=404, detail="Training exercise item not found")

    await session.delete(item)
    await session.flush()
