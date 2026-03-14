"""Configuration helpers for the tyre sentiment CLI."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
GOOGLE_NEWS_RSS_BASE_URL = "https://news.google.com/rss/search"
BRANDS = ("CEAT", "MRF", "Apollo", "TVS", "JK")
BRAND_QUERIES = {
    "CEAT": "ceat tyres",
    "MRF": "mrf tyres",
    "Apollo": "apollo tyres",
    "TVS": "tvs tyres",
    "JK": "jk tyre",
}


@dataclass(slots=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    openai_api_key: str
    openai_model: str = DEFAULT_OPENAI_MODEL
    google_news_rss_base_url: str = GOOGLE_NEWS_RSS_BASE_URL
    request_timeout: int = 30


def get_settings() -> Settings:
    """Load settings from environment variables."""

    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    openai_model = os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL).strip() or DEFAULT_OPENAI_MODEL

    missing = []
    if not openai_api_key:
        missing.append("OPENAI_API_KEY")

    if missing:
        missing_text = ", ".join(missing)
        raise ValueError(f"Missing required environment variables: {missing_text}")

    return Settings(
        openai_api_key=openai_api_key,
        openai_model=openai_model,
    )
