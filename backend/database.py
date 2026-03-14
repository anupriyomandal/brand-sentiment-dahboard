"""Database configuration and session helpers."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.config import get_settings


settings = get_settings()


class Base(DeclarativeBase):
    """Base class for ORM models."""


engine = create_engine(settings.database_url, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Generator[Session, None, None]:
    """Yield a transactional database session."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
