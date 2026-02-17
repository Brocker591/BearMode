from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.body_category import BodyCategory
from app.features.body_category.schemas import BodyCategoryUpdate, BodyCategoryResponse


router = APIRouter()


@router.put("/body-categories", response_model=BodyCategoryResponse, tags=["body-categories"])
async def update_body_category(body: BodyCategoryUpdate, session: AsyncSession = Depends(get_session)) -> BodyCategoryResponse:
    
    category = (await session.execute(
        select(BodyCategory)
        .where(BodyCategory.id == body.id)
    )).scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=404, detail="Body Category not found")

    # Check if name already exists for another category
    existing_name = (await session.execute(
        select(BodyCategory)
        .where(BodyCategory.name == body.name)
        .where(BodyCategory.id != body.id)
    )).scalar_one_or_none()

    if existing_name is not None:
        raise HTTPException(status_code=409, detail="Name already exists")

    category.name = body.name
    
    await session.flush()
    await session.refresh(category)

    return BodyCategoryResponse.model_validate(category)
