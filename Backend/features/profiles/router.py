from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ...infrastructure.database import get_db
from .schemas import ProfileCreate, ProfileResponse, ProfileBase
from .usecase import ProfileUseCase

router = APIRouter(
    prefix="/profiles",
    tags=["profiles"]
)

def get_profile_use_case(db: AsyncSession = Depends(get_db)) -> ProfileUseCase:
    return ProfileUseCase(db)

@router.post("/", response_model=ProfileResponse)
async def create_profile(
    profile: ProfileCreate, 
    use_case: ProfileUseCase = Depends(get_profile_use_case)
):
    return await use_case.create_profile(profile)

@router.get("/{profile_id}", response_model=ProfileResponse)
async def read_profile(
    profile_id: int, 
    use_case: ProfileUseCase = Depends(get_profile_use_case)
):
    return await use_case.get_profile(profile_id)

@router.get("/", response_model=List[ProfileResponse])
async def read_profiles(
    skip: int = 0, 
    limit: int = 100, 
    use_case: ProfileUseCase = Depends(get_profile_use_case)
):
    return await use_case.get_profiles(skip, limit)

@router.put("/{profile_id}", response_model=ProfileResponse)
async def update_profile(
    profile_id: int, 
    profile_update: ProfileBase, 
    use_case: ProfileUseCase = Depends(get_profile_use_case)
):
    return await use_case.update_profile(profile_id, profile_update)

@router.delete("/{profile_id}", response_model=ProfileResponse)
async def delete_profile(
    profile_id: int, 
    use_case: ProfileUseCase = Depends(get_profile_use_case)
):
    return await use_case.delete_profile(profile_id)
