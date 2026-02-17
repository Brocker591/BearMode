from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.body_category import BodyCategory
from app.features.body_category.schemas import BodyCategoryResponse


router = APIRouter()


@router.get("/body-categories", response_model=list[BodyCategoryResponse], status_code=200, tags=["body-categories"])
async def list_body_categories(session: AsyncSession = Depends(get_session)) -> list[BodyCategoryResponse]:

    all_categories = await session.execute(
        select(BodyCategory)
        .order_by(BodyCategory.name)
    )
    result = list(all_categories.scalars().all())

    return [BodyCategoryResponse.model_validate(category) for category in result]
