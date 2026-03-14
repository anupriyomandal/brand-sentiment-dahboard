"""SQLAlchemy ORM models."""

from __future__ import annotations

from datetime import UTC, datetime, date

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class Article(Base):
    """Stored news article."""

    __tablename__ = "articles"
    __table_args__ = (UniqueConstraint("headline", "source", name="uq_articles_headline_source"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    brand: Mapped[str] = mapped_column(String(50), index=True)
    headline: Mapped[str] = mapped_column(String(500))
    source: Mapped[str] = mapped_column(String(200), default="Unknown")
    url: Mapped[str] = mapped_column(String(1000), unique=True)
    sentiment: Mapped[str] = mapped_column(String(20), index=True)
    topic: Mapped[str] = mapped_column(String(50), index=True)
    published_date: Mapped[date] = mapped_column(Date, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class DailySentiment(Base):
    """Daily sentiment aggregate per brand."""

    __tablename__ = "daily_sentiment"
    __table_args__ = (UniqueConstraint("brand", "date", name="uq_daily_sentiment_brand_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    brand: Mapped[str] = mapped_column(String(50), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    articles: Mapped[int] = mapped_column(Integer, default=0)
    positive: Mapped[int] = mapped_column(Integer, default=0)
    neutral: Mapped[int] = mapped_column(Integer, default=0)
    negative: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[float] = mapped_column(Float, default=0.0)


class PipelineRun(Base):
    """One execution of the ingestion pipeline."""

    __tablename__ = "pipeline_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    status: Mapped[str] = mapped_column(String(30), default="running", index=True)
    total_fetched: Mapped[int] = mapped_column(Integer, default=0)
    total_processed: Mapped[int] = mapped_column(Integer, default=0)
    total_added: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    brand_progress: Mapped[list["PipelineBrandProgress"]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan",
    )


class PipelineBrandProgress(Base):
    """Brand-level progress for one pipeline run."""

    __tablename__ = "pipeline_brand_progress"
    __table_args__ = (UniqueConstraint("run_id", "brand", name="uq_pipeline_brand_progress_run_brand"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("pipeline_runs.id", ondelete="CASCADE"), index=True)
    brand: Mapped[str] = mapped_column(String(50), index=True)
    fetched: Mapped[int] = mapped_column(Integer, default=0)
    processed: Mapped[int] = mapped_column(Integer, default=0)
    added: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    run: Mapped[PipelineRun] = relationship(back_populates="brand_progress")
