from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import DB_URL


engine = create_engine(
    DB_URL,
    connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()