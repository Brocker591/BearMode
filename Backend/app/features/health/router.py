from fastapi import APIRouter

from app.features.health.schemas import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    return HealthResponse(status="ok")
