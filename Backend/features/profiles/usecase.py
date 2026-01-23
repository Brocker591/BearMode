from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from fastapi import HTTPException

from .models import Profile
from .schemas import ProfileCreate, ProfileBase

class ProfileUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_profile(self, profile: ProfileCreate) -> Profile:
        db_profile = Profile(name=profile.name)
        self.db.add(db_profile)
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile

    async def get_profile(self, profile_id: int) -> Profile:
        result = await self.db.execute(select(Profile).where(Profile.id == profile_id))
        profile = result.scalars().first()
        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile

    async def get_profiles(self, skip: int = 0, limit: int = 100) -> List[Profile]:
        result = await self.db.execute(select(Profile).offset(skip).limit(limit))
        profiles = result.scalars().all()
        return profiles

    async def update_profile(self, profile_id: int, profile_update: ProfileBase) -> Profile:
        db_profile = await self.get_profile(profile_id)
        db_profile.name = profile_update.name
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile

    async def delete_profile(self, profile_id: int) -> Profile:
        db_profile = await self.get_profile(profile_id)
        await self.db.delete(db_profile)
        await self.db.commit()
        return db_profile
