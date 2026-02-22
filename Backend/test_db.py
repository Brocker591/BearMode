import asyncio
from sqlalchemy import select
from app.infrastructure.database import async_session_maker
from app.Models.training_plan import TrainingPlan

async def main():
    async with async_session_maker() as session:
        plans = (await session.execute(select(TrainingPlan.id))).scalars().all()
        print("Plan IDs:", plans)

if __name__ == "__main__":
    asyncio.run(main())
