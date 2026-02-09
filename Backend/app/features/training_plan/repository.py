from math import e
from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.Models.training_exercise_item import TrainingExerciseItem
from app.Models.training_plan import TrainingPlan, TrainingExercise
from app.features.training_plan.schemas import TrainingPlanCreate


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

# Noch zu überarbeiten


async def get_by_id(session: AsyncSession, plan_id: UUID) -> TrainingPlan | None:
    result = await session.execute(
        select(TrainingPlan)
        .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
        .where(TrainingPlan.id == plan_id)
    )
    return result.scalar_one_or_none()


async def get_all(session: AsyncSession) -> list[TrainingPlan]:
    result = await session.execute(
        select(TrainingPlan)
        .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
        .order_by(TrainingPlan.name)
    )
    return list(result.scalars().all())


async def update(session: AsyncSession, plan_id: UUID, name: str | None, profile_id: UUID | None, exercises_data: list | None) -> TrainingPlan | None:
    plan = await get_by_id(session, plan_id)
    if plan is None:
        return None

    if name is not None:
        plan.name = name
    if profile_id is not None:
        plan.profile_id = profile_id

    if exercises_data is not None:
        # Replace exercises strategy: Delete existing and re-create
        # Alternatively, we could diff them, but usually replacement is easier for whole-plan updates.
        # Note: This deletes *TrainingExercise* rows, not the items.

        # Remove old exercises
        # We need to explicitly delete them if cascade doesn't handle it in memory or to be safe
        # session.delete on the parent might not delete children if not configured,
        # but here we are modifying the collection.

        # Easiest way with SQLAlchemy ORM:
        plan.exercises.clear()

        for exercise_dto in exercises_data:
            # Determine item_id
            item_id = exercise_dto.training_exercise_item_id
            if not item_id and exercise_dto.training_exercise_item:
                item_id = exercise_dto.training_exercise_item.item_id

            new_exercise = TrainingExercise(
                training_plan_id=plan.id,
                order=exercise_dto.order,
                equipment=exercise_dto.equipment,
                sets=exercise_dto.sets,
                reps=exercise_dto.reps,
                break_time_seconds=exercise_dto.break_time_seconds,
                training_exercise_item_id=item_id
            )
            # We can append to the relationship
            plan.exercises.append(new_exercise)

    await session.flush()

    # Reload the plan with all nested relationships loaded
    result = await session.execute(
        select(TrainingPlan)
        .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
        .where(TrainingPlan.id == plan_id)
    )
    return result.scalar_one()


async def delete(session: AsyncSession, plan_id: UUID) -> bool:
    plan = await get_by_id(session, plan_id)
    if plan is None:
        return False
    await session.delete(plan)
    await session.flush()
    return True
