import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes.models import Base

DATABASE_URL = os.getenv("DATABASE_URL")

class Database():
    def __init__(self):
        self.engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False)

        self.session = SessionLocal()
        Base.metadata.create_all(bind=self.engine)

    def close(self):
        self.session.close()

    def add(self, model):
        if model:
            self.session.add(model)
            self.session.commit()

    def get_all(self, query):
        return self.session.execute(query).all()

    def get_first(self, query):
        result = self.session.execute(query).first()
        if result:
            return result[0]
        else:
            return None

    def delete(self, model):
        if model:
            self.session.delete(model)
            self.session.commit()