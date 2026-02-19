
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.Models.body_category import BodyCategory

DEFAULT_CATEGORIES = [
    "Brust",
    "Rücken",
    "Beine",
    "Schultern",
    "Arme",
    "Bauch",
    "Unterer Rücken"
]

async def init_db(session: AsyncSession) -> None:
    # Check if any categories exist
    result = await session.execute(select(BodyCategory).limit(1))
    existing = result.scalar_one_or_none()
    
    if existing is None:
        print("Seeding default body categories...")
        for name in DEFAULT_CATEGORIES:
            category = BodyCategory(name=name)
            session.add(category)
        
        await session.commit()
        print("Seeding complete.")
    else:
        print("Body categories already exist. Skipping seed.")
