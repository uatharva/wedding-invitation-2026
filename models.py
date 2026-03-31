from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class RSVP(Base):
    __tablename__ = "rsvps"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    full_name = Column(String(256), nullable=False)
    attending = Column(String(32), nullable=True)
    guest_count = Column(Integer, nullable=True)
    meal_preference = Column(String(128), nullable=True)
    dietary_restrictions = Column(String(256), nullable=True)
    song_request = Column(String(256), nullable=True)
    message = Column(Text, nullable=True)


def init_db(database_url: str = None):
    """Create engine, SessionLocal and ensure tables exist.

    The function returns (engine, SessionLocal).
    """
    if database_url is None:
        database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        # default to local sqlite file
        database_url = f"sqlite:///{os.path.join(os.getcwd(), 'rsvps.db')}"

    connect_args = {}
    if database_url.startswith("sqlite:"):
        connect_args = {"check_same_thread": False}

    engine = create_engine(database_url, echo=False, future=True, connect_args=connect_args)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    # Create tables
    Base.metadata.create_all(bind=engine)

    return engine, SessionLocal
