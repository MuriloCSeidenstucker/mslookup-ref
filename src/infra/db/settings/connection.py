from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(
    "sqlite:///mslookup.db",
    pool_pre_ping=True,
)


def get_session():
    with Session(engine, expire_on_commit=False) as session:
        yield session


def get_engine():
    return engine
