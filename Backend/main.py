from fastapi import FastAPI
from infrastructure.database import engine, Base
from features.profiles import router as profiles_router

app = FastAPI()

@app.lifespan("startup")
def startup():
    # create db tables
    Base.metadata.create_all(bind=engine)

app.include_router(profiles_router.router)
