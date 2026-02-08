from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.training_plan.models import TrainingPlan, TrainingExercise


async def create(session: AsyncSession, name: str, profile_id: UUID, exercises_data: list) -> TrainingPlan:
    new_plan = TrainingPlan(name=name, profile_id=profile_id)
    # session.add(new_plan) 
    # Not strictly needed to add before appending if using relationship, 
    # but good for ensuring ID if needed early (though we don't strictly need it here if we use append).
    
    for exercise_dto in exercises_data:
        # Determine item_id
        item_id = exercise_dto.training_exercise_item_id
        if not item_id and exercise_dto.training_exercise_item:
            item_id = exercise_dto.training_exercise_item.item_id
        
        new_exercise = TrainingExercise(
            # training_plan_id will be set by append
            order=exercise_dto.order,
            equipment=exercise_dto.equipment,
            sets=exercise_dto.sets,
            reps=exercise_dto.reps,
            break_time_seconds=exercise_dto.break_time_seconds,
            training_exercise_item_id=item_id
        )
        new_plan.exercises.append(new_exercise)

    session.add(new_plan)
    await session.flush()
    await session.refresh(new_plan, attribute_names=["exercises"])
    return new_plan


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
    await session.refresh(plan, attribute_names=["exercises"])
    return plan


async def delete(session: AsyncSession, plan_id: UUID) -> bool:
    plan = await get_by_id(session, plan_id)
    if plan is None:
        return False
    await session.delete(plan)
    await session.flush()
    return True
