from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.repository import ProfileRepository
from app.features.profiles.schemas import ProfileCreate, ProfileResponse, ProfileUpdate
from app.infrastructure.database import get_session

router = APIRouter()


@router.post("", response_model=ProfileResponse, status_code=201)
async def post_profile(body: ProfileCreate, session: AsyncSession = Depends(get_session)) -> ProfileResponse:
    existing = await ProfileRepository.get_by_name(session, body.name)
    if existing is not None:
        raise HTTPException(status_code=409, detail="Name already exists")
    profile = await ProfileRepository.create(session, body.name)
    return ProfileResponse.model_validate(profile)


@router.get("", response_model=list[ProfileResponse])
async def list_profiles(session: AsyncSession = Depends(get_session)) -> list[ProfileResponse]:
    profiles = await ProfileRepository.get_all(session)
    return [ProfileResponse.model_validate(p) for p in profiles]


@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile(profile_id: UUID, session: AsyncSession = Depends(get_session)) -> ProfileResponse:
    profile = await ProfileRepository.get_by_id(session, profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileResponse.model_validate(profile)


@router.put("/{profile_id}", response_model=ProfileResponse)
async def put_profile(profile_id: UUID, body: ProfileUpdate, session: AsyncSession = Depends(get_session)) -> ProfileResponse:
    profile = await ProfileRepository.update(session, profile_id, body.name)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileResponse.model_validate(profile)


@router.delete("/{profile_id}", status_code=204)
async def delete_profile_endpoint(profile_id: UUID, session: AsyncSession = Depends(get_session)) -> None:
    deleted = await ProfileRepository.delete(session, profile_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Profile not found")
