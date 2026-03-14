"""Application configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
BRANDS = ("CEAT", "MRF", "Apollo", "TVS", "JK")
BRAND_QUERIES = {
    "CEAT": "ceat tyres",
    "MRF": "mrf tyres",
    "Apollo": "apollo tyres",
    "TVS": "tvs tyres",
    "JK": "jk tyre",
}
TOPICS = (
    "Product Launch",
    "Earnings",
    "Exports",
    "Market Expansion",
    "Cost Pressure",
    "EV Tyres",
    "Regulation",
    "Other",
)


def normalize_database_url(raw_url: str) -> str:
    """Normalize Railway/Postgres URLs to the SQLAlchemy psycopg dialect."""

    url = raw_url.strip()
    if not url:
        return "sqlite:///./tyre_intelligence.db"
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://") and "+psycopg" not in url:
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


@dataclass(slots=True)
class Settings:
    """Settings loaded from environment variables."""

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "").strip()
    openai_model: str = os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL).strip() or DEFAULT_OPENAI_MODEL
    database_url: str = normalize_database_url(
        os.getenv(
            "DATABASE_URL",
            "sqlite:///./tyre_intelligence.db",
        )
    )
    redis_url: str = os.getenv("REDIS_URL", "").strip()
    request_timeout: int = 30
    google_news_rss_base_url: str = "https://news.google.com/rss/search"


def get_settings() -> Settings:
    """Return runtime settings."""

    return Settings()
