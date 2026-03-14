"""Shared service models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, date, datetime


@dataclass(slots=True)
class NewsArticle:
    brand: str
    headline: str
    source: str
    url: str
    published_date: date


@dataclass(slots=True)
class AnalysedArticle:
    brand: str
    headline: str
    source: str
    url: str
    sentiment: str
    topic: str
    published_date: date
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
