from math import e
from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.Models.training_exercise_item import TrainingExerciseItem
from app.Models.training_plan import TrainingPlan, TrainingExercise
from app.features.training_plan.schemas import TrainingPlanCreate, TrainingPlanUpdate


async def create(session: AsyncSession, training_plan: TrainingPlanCreate) -> TrainingPlan:

    training_plan_id = uuid4()
    exercises_data = []

    for exercise_dto in training_plan.training_exercises:

        exercise_item_exists = (await session.execute(
            select(TrainingExerciseItem)
            .where(TrainingExerciseItem.id == exercise_dto.training_exercise_item_id)
        )).scalar_one_or_none()

        if not exercise_item_exists:
            raise ValueError(
                f"TrainingExerciseItem with id {exercise_dto.training_exercise_item_id} does not exist")

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
    result = await session.execute(
        select(TrainingPlan)
        .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
        .where(TrainingPlan.id == training_plan_id)
    )
    return result.scalar_one()


async def get_by_id(session: AsyncSession, plan_id: UUID) -> TrainingPlan | None:
    result = await session.execute(
        select(TrainingPlan)
        .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
        .where(TrainingPlan.id == plan_id)
    )
    return result.scalar_one_or_none()


async def get_all(session: AsyncSession) -> list[TrainingPlan]:
    all_plans = await session.execute(
        select(TrainingPlan)
        .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
        .order_by(TrainingPlan.name)
    )
    result = list(all_plans.scalars().all())
    return result


async def update(session: AsyncSession, training_plan: TrainingPlanUpdate) -> TrainingPlan | None:
    plan = await get_by_id(session, training_plan.id)
    if plan is None:
        return None

    plan.name = training_plan.name
    plan.profile_id = training_plan.profile_id

    # Clear existing exercises
    plan.exercises.clear()

    for exercise_dto in training_plan.training_exercises:

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
    result = await session.execute(
        select(TrainingPlan)
        .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
        .where(TrainingPlan.id == training_plan.id)
    )
    return result.scalar_one()


async def delete(session: AsyncSession, plan_id: UUID) -> bool:
    plan = await get_by_id(session, plan_id)
    if plan is None:
        return False
    await session.delete(plan)
    await session.flush()
    return True
