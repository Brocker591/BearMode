from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.body_category import BodyCategory


router = APIRouter()


@router.delete("/body-categories/{category_id}", status_code=204, tags=["body-categories"])
async def delete_body_category(category_id: UUID, session: AsyncSession = Depends(get_session)) -> None:

    category = (await session.execute(
        select(BodyCategory)
        .where(BodyCategory.id == category_id)
    )).scalar_one_or_none()

    if category is None:
        raise HTTPException(status_code=404, detail="Body Category not found")

    await session.delete(category)
    await session.flush()
