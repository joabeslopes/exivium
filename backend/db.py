import os
from sqalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DTABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://exivium:exivium@db:5432/exivium",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

