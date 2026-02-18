from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.profile import Profile
from app.features.profiles.schemas import ProfileResponse


router = APIRouter()


@router.get("/profiles", response_model=list[ProfileResponse], status_code=200, tags=["profiles"])
async def list_profiles(session: AsyncSession = Depends(get_session)) -> list[ProfileResponse]:

    all_profiles = await session.execute(
        select(Profile)
        .order_by(Profile.name)
    )
    result = list(all_profiles.scalars().all())

    return [ProfileResponse.model_validate(p) for p in result]
