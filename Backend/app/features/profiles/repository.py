from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.profiles.models import Profile


async def create(session: AsyncSession, name: str) -> Profile:
    profile = Profile(name=name)
    session.add(profile)
    await session.flush()
    await session.refresh(profile)
    return profile


async def get_by_id(session: AsyncSession, profile_id: UUID) -> Profile | None:
    result = await session.execute(select(Profile).where(Profile.id == profile_id))
    return result.scalar_one_or_none()


async def get_all(session: AsyncSession) -> list[Profile]:
    result = await session.execute(select(Profile).order_by(Profile.name))
    return list(result.scalars().all())


async def get_by_name(session: AsyncSession, name: str) -> Profile | None:
    result = await session.execute(select(Profile).where(Profile.name == name))
    return result.scalar_one_or_none()


async def update(
    session: AsyncSession, profile_id: UUID, name: str | None
) -> Profile | None:
    profile = await get_by_id(session, profile_id)
    if profile is None:
        return None
    if name is not None:
        profile.name = name
    await session.flush()
    await session.refresh(profile)
    return profile


async def delete(session: AsyncSession, profile_id: UUID) -> bool:
    profile = await get_by_id(session, profile_id)
    if profile is None:
        return False
    await session.delete(profile)
    await session.flush()
    return True
