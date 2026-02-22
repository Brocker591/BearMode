from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.profile import Profile
from app.features.profiles.schemas import ProfileUpdate, ProfileResponse


router = APIRouter()


@router.put("/profiles/{profile_id}", response_model=ProfileResponse, tags=["profiles"])
async def update_profile(profile_id: UUID, body: ProfileUpdate, session: AsyncSession = Depends(get_session)) -> ProfileResponse:
    
    profile = (await session.execute(
        select(Profile)
        .where(Profile.id == profile_id)
    )).scalar_one_or_none()

    if profile is None:
        raise HTTPException(
            status_code=404, detail="Profile not found")

    if body.name is not None:
        # Check if name already exists for another profile
        existing_name = (await session.execute(
            select(Profile)
            .where(Profile.name == body.name)
            .where(Profile.id != profile_id)
        )).scalar_one_or_none()

        if existing_name is not None:
            raise HTTPException(status_code=409, detail="Name already exists")

        profile.name = body.name

    if body.emoji is not None:
        profile.emoji = body.emoji
    
    await session.flush()
    await session.refresh(profile)

    return ProfileResponse.model_validate(profile)
