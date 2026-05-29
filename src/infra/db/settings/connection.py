import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()
db_url = os.getenv("DATABASE_URL", "sqlite:///mslookup.db")
engine = create_engine(
    db_url,
    pool_pre_ping=True,
)


def get_session():
    with Session(engine, expire_on_commit=False) as session:
        yield session


def get_engine():
    return engine
