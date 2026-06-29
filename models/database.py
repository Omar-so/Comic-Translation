# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
from config import settings
engine = create_engine(settings.db_url, echo=True)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()