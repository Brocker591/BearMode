from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.profile import Profile


router = APIRouter()


@router.delete("/profiles/{profile_id}", status_code=204, tags=["profiles"])
async def delete_profile(profile_id: UUID, session: AsyncSession = Depends(get_session)) -> None:

    profile = (await session.execute(
        select(Profile)
        .where(Profile.id == profile_id)
    )).scalar_one_or_none()

    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    await session.delete(profile)
    await session.flush()
