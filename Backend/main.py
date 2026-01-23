from fastapi import FastAPI
from .infrastructure.database import engine, Base
from .features.profiles import router as profiles_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(profiles_router.router)
