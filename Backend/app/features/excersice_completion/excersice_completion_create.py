from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.training_exercise_completion import TrainingExerciseCompletion as TrainingExerciseCompletionModel
from app.features.excersice_completion.schemas import TrainingExerciseCompletion
from app.Models.profile import Profile
from app.Models.training_plan import TrainingPlan, TrainingExercise


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


@router.post("/exercice-completion", status_code=201, tags=["exercice-completion"])
async def create_training_plan(exercise_compeltions: list[TrainingExerciseCompletion], session: AsyncSession = Depends(get_session)) -> None:
    try:
        # Collect unique IDs
        profile_ids = {ec.profile_id for ec in exercise_compeltions}
        training_plan_ids = {
            ec.training_plan_id for ec in exercise_compeltions}
        exercise_ids = {ec.exercise_id for ec in exercise_compeltions}

        # Validate existence
        await validate_ids(session, Profile, profile_ids, "Profile")
        await validate_ids(session, TrainingPlan, training_plan_ids, "TrainingPlan")
        await validate_ids(session, TrainingExercise, exercise_ids, "TrainingExercise")

        for exercise_completion in exercise_compeltions:
            completion = TrainingExerciseCompletionModel(
                id=exercise_completion.id or uuid4(),
                profile_id=exercise_completion.profile_id,
                training_plan_id=exercise_completion.training_plan_id,
                exercise_id=exercise_completion.exercise_id,
                order=exercise_completion.order,
                equipment=exercise_completion.equipment,
                reps=exercise_completion.reps,
                break_time_seconds=exercise_completion.break_time_seconds,
                training_exercise_description=exercise_completion.training_exercise_description,
                training_exercise_video_url=exercise_completion.training_exercise_video_url,
                created_at=datetime.now(),
                training_day=exercise_completion.training_day or datetime.now().date()
            )
            session.add(completion)

        await session.flush()

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
