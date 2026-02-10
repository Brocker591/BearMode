from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.training_exercise_item import TrainingExerciseItem
from app.Models.training_plan import TrainingPlan, TrainingExercise
from app.features.training_plan.schemas import TrainingPlanUpdate, TrainingPlanResponse


router = APIRouter()


@router.put("/training-plans", response_model=TrainingPlanResponse, tags=["training-plans"])
async def update_training_plan(training_plan_update: TrainingPlanUpdate, session: AsyncSession = Depends(get_session)) -> TrainingPlanResponse:
    try:

        plan = (await session.execute(
            select(TrainingPlan)
            .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
            .where(TrainingPlan.id == training_plan_update.id)
        )).scalar_one_or_none()

        if plan is None:
            raise HTTPException(
                status_code=404, detail="Training Plan not found")

        plan.name = training_plan_update.name
        plan.profile_id = training_plan_update.profile_id

        # Clear existing exercises
        plan.exercises.clear()

        for exercise_dto in training_plan_update.training_exercises:

            exercise_item_exists = (await session.execute(
                select(TrainingExerciseItem)
                .where(TrainingExerciseItem.id == exercise_dto.training_exercise_item_id)
            )).scalar_one_or_none()

            if not exercise_item_exists:
                raise ValueError(
                    f"TrainingExerciseItem with id {exercise_dto.training_exercise_item_id} does not exist")

            new_exercise = TrainingExercise(
                id=uuid4(),
                training_plan_id=plan.id,
                order=exercise_dto.order,
                equipment=exercise_dto.equipment,
                sets=exercise_dto.sets,
                reps=exercise_dto.reps,
                break_time_seconds=exercise_dto.break_time_seconds,
                training_exercise_item_id=exercise_dto.training_exercise_item_id,
                training_exercise_item=exercise_item_exists
            )
            plan.exercises.append(new_exercise)

        await session.flush()

        # Reload the plan with all nested relationships loaded
        result = (await session.execute(
            select(TrainingPlan)
            .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
            .where(TrainingPlan.id == training_plan_update.id)
        )).scalar_one()

        return TrainingPlanResponse.model_validate(result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
