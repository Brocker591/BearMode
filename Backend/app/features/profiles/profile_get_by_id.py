from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.profile import Profile
from app.features.profiles.schemas import ProfileResponse


router = APIRouter()


@router.get("/profiles/{profile_id}", response_model=ProfileResponse, status_code=200, tags=["profiles"])
async def get_profile(profile_id: UUID, session: AsyncSession = Depends(get_session)) -> ProfileResponse:

    profile = (await session.execute(
        select(Profile)
        .where(Profile.id == profile_id)
    )).scalar_one_or_none()

    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return ProfileResponse.model_validate(profile)
