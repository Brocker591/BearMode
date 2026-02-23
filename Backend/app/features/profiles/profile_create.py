from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.profile import Profile
from app.features.profiles.schemas import ProfileCreate, ProfileResponse


router = APIRouter()


@router.post("/profiles", response_model=ProfileResponse, status_code=201, tags=["profiles"])
async def create_profile(body: ProfileCreate, session: AsyncSession = Depends(get_session)) -> ProfileResponse:
    
    existing = (await session.execute(
        select(Profile)
        .where(Profile.name == body.name)
    )).scalar_one_or_none()

    if existing is not None:
        raise HTTPException(status_code=409, detail="Name already exists")

    profile = Profile(name=body.name, emoji=body.emoji)
    session.add(profile)
    await session.flush()
    await session.refresh(profile)

    return ProfileResponse.model_validate(profile)
