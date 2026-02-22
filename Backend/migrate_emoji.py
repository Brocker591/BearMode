import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sqlalchemy import text
from app.infrastructure.database import async_session_factory

async def migrate():
    async with async_session_factory() as session:
        try:
            await session.execute(text("ALTER TABLE profiles ADD COLUMN emoji VARCHAR(10);"))
            await session.commit()
            print("Migration successful")
        except Exception as e:
            await session.rollback()
            if "already exists" in str(e):
                print("Column already exists")
            else:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(migrate())
