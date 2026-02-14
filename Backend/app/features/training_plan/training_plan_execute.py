from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.training_plan import TrainingPlan, TrainingExercise
from app.features.training_plan.schemas import TrainingPlanExecuteResponse, TrainingExerciseExecuteResponse


router = APIRouter()


@router.get("/training-plans/{plan_id}/execute", response_model=TrainingPlanExecuteResponse, tags=["training-plans"])
async def get_training_plan(plan_id: UUID, session: AsyncSession = Depends(get_session)) -> TrainingPlanExecuteResponse:

    plan = (await session.execute(
        select(TrainingPlan)
        .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
        .where(TrainingPlan.id == plan_id)
    )).scalar_one_or_none()

    if plan is None:
        raise HTTPException(status_code=404, detail="Training Plan not found")

    exercise_data = []
    order = 1

    for exercise in sorted(plan.exercises, key=lambda e: e.order):
        for set in range(exercise.sets):

            execute_exercise = TrainingExerciseExecuteResponse(
                id=uuid4(),
                exercise_id=exercise.id,
                order=order,
                equipment=exercise.equipment,
                reps=exercise.reps,
                break_time_seconds=exercise.break_time_seconds,
                training_exercise_description=exercise.training_exercise_item.description,
                training_exercise_video_url=exercise.training_exercise_item.video_url
            )

            exercise_data.append(execute_exercise)
            order += 1

    execute_plan = TrainingPlanExecuteResponse(
        id=plan.id,
        name=plan.name,
        profile_id=plan.profile_id,
        exercises=exercise_data
    )

    return execute_plan
