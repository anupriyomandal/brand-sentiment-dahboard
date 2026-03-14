"""Aggregate per-article sentiment results into brand summaries."""

from __future__ import annotations

from config import BRANDS
from models import ArticleResult


def build_summary(results: list[ArticleResult]) -> dict[str, dict[str, float | int]]:
    """Aggregate sentiment counts and score by brand."""

    summary: dict[str, dict[str, float | int]] = {
        brand: {
            "articles": 0,
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "score": 0.0,
        }
        for brand in BRANDS
    }

    for article in results:
        brand_summary = summary[article.brand]
        brand_summary["articles"] += 1
        brand_summary[article.sentiment.lower()] += 1

    for brand, brand_summary in summary.items():
        articles = int(brand_summary["articles"])
        if articles:
            positive = int(brand_summary["positive"])
            negative = int(brand_summary["negative"])
            brand_summary["score"] = round((positive - negative) / articles, 2)
        else:
            brand_summary["score"] = 0.0

    return summary
