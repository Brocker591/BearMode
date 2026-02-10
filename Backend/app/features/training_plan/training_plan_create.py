from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.Models.training_exercise_item import TrainingExerciseItem
from app.Models.training_plan import TrainingPlan, TrainingExercise
from app.features.training_plan.schemas import TrainingPlanCreate, TrainingPlanResponse


router = APIRouter()


@router.post("/training-plans", response_model=TrainingPlanResponse, status_code=201, tags=["training-plans"])
async def create_training_plan(training_plan: TrainingPlanCreate, session: AsyncSession = Depends(get_session)) -> TrainingPlanResponse:
    try:
        training_plan_id = uuid4()
        exercises_data = []

        for exercise_dto in training_plan.training_exercises:

            exercise_item_exists = (await session.execute(select(TrainingExerciseItem)
                                                          .where(TrainingExerciseItem.id == exercise_dto.training_exercise_item_id))).scalar_one_or_none()

            if not exercise_item_exists:
                raise HTTPException(
                    status_code=404,
                    detail=f"TrainingExerciseItem with id {exercise_dto.training_exercise_item_id} does not exist"
                )

            new_exercise = TrainingExercise(
                id=uuid4(),
                training_plan_id=training_plan_id,
                order=exercise_dto.order,
                equipment=exercise_dto.equipment,
                sets=exercise_dto.sets,
                reps=exercise_dto.reps,
                break_time_seconds=exercise_dto.break_time_seconds,
                training_exercise_item_id=exercise_dto.training_exercise_item_id,
                training_exercise_item=exercise_item_exists
            )
            exercises_data.append(new_exercise)

        new_plan = TrainingPlan(
            id=training_plan_id,
            name=training_plan.name,
            profile_id=training_plan.profile_id,
            exercises=exercises_data
        )
        session.add(new_plan)
        await session.flush()

        # Reload the plan with all nested relationships loaded
        result = (await session.execute(
            select(TrainingPlan)
            .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
            .where(TrainingPlan.id == training_plan_id))
        ).scalar_one()

        return TrainingPlanResponse.model_validate(result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
