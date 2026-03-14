"""Data models used across the CLI."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class NewsArticle:
    """Article headline data fetched from Google News RSS."""

    brand: str
    title: str
    link: str
    source: str


@dataclass(slots=True)
class ArticleResult:
    """Article headline data after sentiment classification."""

    brand: str
    title: str
    sentiment: str
