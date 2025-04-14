from sqlalchemy import Column, Integer, BigInteger, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from contextlib import contextmanager
from typing import List

Base = declarative_base()

class LeaderboardEntry(Base):
    __tablename__ = 'leaderboard_entries'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    score = Column(Integer, default=0)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def get_top(cls, limit: int = 10) -> List['LeaderboardEntry']:
        with get_session() as session:
            return session.query(cls)\
                .order_by(cls.score.desc())\
                .limit(limit)\
                .all()

    @classmethod
    def update_score(cls, user_id: int, score: int):
        with get_session() as session:
            entry = session.query(cls)\
                .filter_by(user_id=user_id)\
                .first()
            
            if entry:
                entry.score = score
            else:
                entry = cls(user_id=user_id, score=score)
                session.add(entry)
            
            session.commit()

    @classmethod
    def reset_all(cls):
        with get_session() as session:
            session.query(cls).delete()
            session.commit()

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    team_name = Column(String, unique=True, nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
