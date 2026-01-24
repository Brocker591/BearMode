from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os

DATABASE_URL = os.getenv("DATABASE_URL", "mssql+pyodbc://brocker:QrTPD5f867shMJG@192.168.178.40/DevBearMode?driver=ODBC+Driver+17+for+SQL+Server")

engine = create_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
