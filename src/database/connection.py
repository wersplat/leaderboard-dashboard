from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///leaderboard.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
