from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.Models.training_exercise_item import TrainingExerciseItem



async def create(session: AsyncSession, description: str, video_url: str | None = None) -> TrainingExerciseItem:
    item = TrainingExerciseItem(description=description, video_url=video_url)
    session.add(item)
    # Sendet ausstehende Änderungen (INSERT/UPDATE/DELETE) an die DB
    # innerhalb der aktuellen Transaktion, ohne zu committen.
    # Dadurch werden DB-generierte Werte (z. B. Primärschlüssel) erzeugt.
    await session.flush()
    await session.refresh(item)
    return item


async def get_by_id(session: AsyncSession, item_id: UUID) -> TrainingExerciseItem | None:
    result = await session.execute(select(TrainingExerciseItem).where(TrainingExerciseItem.id == item_id))
    # Gibt genau ein Ergebnis zurück oder None; wirft einen Fehler, wenn >1 Ergebnis existiert.
    return result.scalar_one_or_none()


async def get_all(session: AsyncSession) -> list[TrainingExerciseItem]:
    result = await session.execute(select(TrainingExerciseItem))
    return list(result.scalars().all())

async def get_by_description(session: AsyncSession, description: str) -> TrainingExerciseItem | None:
    result = await session.execute(select(TrainingExerciseItem).where(TrainingExerciseItem.description == description))
    return result.scalar_one_or_none()


async def update(session: AsyncSession, item_id: UUID, description: str, video_url: str | None = None) -> TrainingExerciseItem | None:
    item = await get_by_id(session, item_id)
    if item is None:
        return None
    item.description = description
    item.video_url = video_url

    await session.flush()
    await session.refresh(item)
    return item


async def delete(session: AsyncSession, item_id: UUID) -> bool:
    item = await get_by_id(session, item_id)
    if item is None:
        return False
    await session.delete(item)
    await session.flush()
    return True
