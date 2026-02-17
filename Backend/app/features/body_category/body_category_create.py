from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.body_category.schemas import BodyCategoryCreate, BodyCategoryResponse
from app.Models.body_category import BodyCategory
from app.infrastructure.database import get_session

router = APIRouter()


@router.post("/body-categories", response_model=BodyCategoryResponse, status_code=201)
async def post_body_category(body: BodyCategoryCreate, session: AsyncSession = Depends(get_session)) -> BodyCategoryResponse:

    existing = (await session.execute(select(BodyCategory).where(BodyCategory.name == body.name))).scalar_one_or_none()

    if existing is not None:
        raise HTTPException(status_code=409, detail="Name already exists")

    body_category = BodyCategory(name=body.name)
    session.add(body_category)
    await session.flush()
    await session.refresh(body_category)

    return BodyCategoryResponse.model_validate(body_category)
