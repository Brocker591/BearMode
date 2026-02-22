from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.training_plan_completion import TrainingPlanCompletion as TrainingPlanCompletionModel
from app.features.training_plan_completion.schemas import TrainingPlanCompletion
from app.Models.profile import Profile
from app.Models.training_plan import TrainingPlan

router = APIRouter()

async def validate_ids(session: AsyncSession, model, ids: set[UUID], model_name: str):
    if not ids:
        return

    result = await session.scalars(select(model.id).where(model.id.in_(ids)))
    found_ids = set(result.all())

    missing_ids = ids - found_ids
    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"{model_name} with ids {', '.join(str(id) for id in missing_ids)} not found"
        )

@router.post("/training-plan-completion", status_code=201, tags=["training-plan-completion"])
async def create_training_plan_completion(plan_completions: list[TrainingPlanCompletion], session: AsyncSession = Depends(get_session)) -> None:
    try:
        # Collect unique IDs
        profile_ids = {pc.profile_id for pc in plan_completions}
        training_plan_ids = {pc.training_plan_id for pc in plan_completions}

        # Validate existence
        await validate_ids(session, Profile, profile_ids, "Profile")
        await validate_ids(session, TrainingPlan, training_plan_ids, "TrainingPlan")

        for plan_completion in plan_completions:
            completion = TrainingPlanCompletionModel(
                id=plan_completion.id or uuid4(),
                profile_id=plan_completion.profile_id,
                training_plan_id=plan_completion.training_plan_id,
                training_plan_name=plan_completion.training_plan_name,
                count_completed_exercises=plan_completion.count_completed_exercises,
                count_open_exercises=plan_completion.count_open_exercises,
                created_at=datetime.now(),
                training_day=plan_completion.training_day or datetime.now().date()
            )
            session.add(completion)

        await session.flush()

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
