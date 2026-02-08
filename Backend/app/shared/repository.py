from uuid import UUID
from math import e

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.Models.profile import Profile
from app.Models.training_exercise_item import TrainingExerciseItem
from app.Models.training_plan import TrainingPlan, TrainingExercise


class ProfileRepository:
    @staticmethod
    async def create(session: AsyncSession, name: str) -> Profile:
        profile = Profile(name=name)
        session.add(profile)
        await session.flush()
        await session.refresh(profile)
        return profile

    @staticmethod
    async def get_by_id(session: AsyncSession, profile_id: UUID) -> Profile | None:
        result = await session.execute(select(Profile).where(Profile.id == profile_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession) -> list[Profile]:
        result = await session.execute(select(Profile).order_by(Profile.name))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_name(session: AsyncSession, name: str) -> Profile | None:
        result = await session.execute(select(Profile).where(Profile.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(session: AsyncSession, profile_id: UUID, name: str | None) -> Profile | None:
        profile = await ProfileRepository.get_by_id(session, profile_id)
        if profile is None:
            return None
        if name is not None:
            profile.name = name
        await session.flush()
        await session.refresh(profile)
        return profile

    @staticmethod
    async def delete(session: AsyncSession, profile_id: UUID) -> bool:
        profile = await ProfileRepository.get_by_id(session, profile_id)
        if profile is None:
            return False
        await session.delete(profile)
        await session.flush()
        return True


class TrainingExerciseItemRepository:
    @staticmethod
    async def create(session: AsyncSession, description: str, video_url: str | None = None) -> TrainingExerciseItem:
        item = TrainingExerciseItem(description=description, video_url=video_url)
        session.add(item)
        # Sendet ausstehende Änderungen (INSERT/UPDATE/DELETE) an die DB
        # innerhalb der aktuellen Transaktion, ohne zu committen.
        # Dadurch werden DB-generierte Werte (z. B. Primärschlüssel) erzeugt.
        await session.flush()
        await session.refresh(item)
        return item

    @staticmethod
    async def get_by_id(session: AsyncSession, item_id: UUID) -> TrainingExerciseItem | None:
        result = await session.execute(select(TrainingExerciseItem).where(TrainingExerciseItem.id == item_id))
        # Gibt genau ein Ergebnis zurück oder None; wirft einen Fehler, wenn >1 Ergebnis existiert.
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession) -> list[TrainingExerciseItem]:
        result = await session.execute(select(TrainingExerciseItem))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_description(session: AsyncSession, description: str) -> TrainingExerciseItem | None:
        result = await session.execute(select(TrainingExerciseItem).where(TrainingExerciseItem.description == description))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(session: AsyncSession, item_id: UUID, description: str, video_url: str | None = None) -> TrainingExerciseItem | None:
        item = await TrainingExerciseItemRepository.get_by_id(session, item_id)
        if item is None:
            return None
        item.description = description
        item.video_url = video_url

        await session.flush()
        await session.refresh(item)
        return item

    @staticmethod
    async def delete(session: AsyncSession, item_id: UUID) -> bool:
        item = await TrainingExerciseItemRepository.get_by_id(session, item_id)
        if item is None:
            return False
        await session.delete(item)
        await session.flush()
        return True


class TrainingPlanRepository:
    @staticmethod
    async def create(session: AsyncSession, name: str, profile_id: UUID, exercises_data: list) -> TrainingPlan:
        new_plan = TrainingPlan(name=name, profile_id=profile_id)
        # session.add(new_plan)
        # Not strictly needed to add before appending if using relationship,
        # but good for ensuring ID if needed early (though we don't strictly need it here if we use append).

        print(f"Repository create called with {len(exercises_data)} exercises")
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

        print(
            f"Pre-flush: Plan ID: {new_plan.id}, Exercises: {len(new_plan.exercises)}")
        session.add(new_plan)
        await session.flush()
        print(f"Post-flush: Plan ID: {new_plan.id}")

        # Re-fetch the plan with all relationships loaded
        result_plan = await TrainingPlanRepository.get_by_id(session, new_plan.id)
        print(
            f"Post-fetch: Plan ID: {result_plan.id}, Exercises: {len(result_plan.exercises)}")
        return result_plan

    @staticmethod
    async def get_by_id(session: AsyncSession, plan_id: UUID) -> TrainingPlan | None:
        result = await session.execute(
            select(TrainingPlan)
            .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
            .where(TrainingPlan.id == plan_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession) -> list[TrainingPlan]:
        result = await session.execute(
            select(TrainingPlan)
            .options(selectinload(TrainingPlan.exercises).selectinload(TrainingExercise.training_exercise_item))
            .order_by(TrainingPlan.name)
        )
        return list(result.scalars().all())

    @staticmethod
    async def update(session: AsyncSession, plan_id: UUID, name: str | None, profile_id: UUID | None, exercises_data: list | None) -> TrainingPlan | None:
        plan = await TrainingPlanRepository.get_by_id(session, plan_id)
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

    @staticmethod
    async def delete(session: AsyncSession, plan_id: UUID) -> bool:
        plan = await TrainingPlanRepository.get_by_id(session, plan_id)
        if plan is None:
            return False
        await session.delete(plan)
        await session.flush()
        return True
