from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.body_category import BodyCategory
from app.features.body_category.schemas import BodyCategoryResponse


router = APIRouter()


@router.get("/body-categories/{category_id}", response_model=BodyCategoryResponse, status_code=200, tags=["body-categories"])
async def get_body_category(category_id: UUID, session: AsyncSession = Depends(get_session)) -> BodyCategoryResponse:

    category = (await session.execute(
        select(BodyCategory)
        .where(BodyCategory.id == category_id)
    )).scalar_one_or_none()

    if category is None:
        raise HTTPException(status_code=404, detail="Body Category not found")

    return BodyCategoryResponse.model_validate(category)
