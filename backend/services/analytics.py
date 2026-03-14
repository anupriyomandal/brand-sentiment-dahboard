"""Shared analytics helpers used by the API and CLI."""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime, timedelta

from sqlalchemy import case, desc, func, select
from sqlalchemy.orm import Session

from backend.config import BRANDS
from backend.models import Article, DailySentiment
from backend.schemas import AlertItem, SummaryItem, TopicDistributionItem, TrendPoint
from backend.services.common import AnalysedArticle


def build_summary_from_articles(results: list[AnalysedArticle]) -> dict[str, dict[str, float | int]]:
    """Aggregate a list of analysed articles into the CLI summary shape."""

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
        summary[article.brand]["articles"] += 1
        summary[article.brand][article.sentiment.lower()] += 1

    for brand_summary in summary.values():
        total = int(brand_summary["articles"])
        if total:
            brand_summary["score"] = round(
                (int(brand_summary["positive"]) - int(brand_summary["negative"])) / total,
                2,
            )

    return summary


def fetch_summary(db: Session) -> list[SummaryItem]:
    """Build a sentiment summary from stored articles."""

    rows = db.execute(
        select(
            Article.brand,
            func.count(Article.id),
            func.sum(case((Article.sentiment == "Positive", 1), else_=0)),
            func.sum(case((Article.sentiment == "Neutral", 1), else_=0)),
            func.sum(case((Article.sentiment == "Negative", 1), else_=0)),
        ).group_by(Article.brand)
    ).all()

    lookup = {
        row[0]: SummaryItem(
            brand=row[0],
            articles=int(row[1] or 0),
            positive=int(row[2] or 0),
            neutral=int(row[3] or 0),
            negative=int(row[4] or 0),
            score=round(((int(row[2] or 0) - int(row[4] or 0)) / int(row[1] or 1)), 2),
        )
        for row in rows
    }

    return [
        lookup.get(
            brand,
            SummaryItem(brand=brand, articles=0, positive=0, neutral=0, negative=0, score=0.0),
        )
        for brand in BRANDS
    ]


def fetch_trends(db: Session) -> dict[str, list[TrendPoint]]:
    """Return trend points by brand."""

    rows = db.execute(select(DailySentiment).order_by(DailySentiment.brand, DailySentiment.date)).scalars().all()
    trends: dict[str, list[TrendPoint]] = defaultdict(list)
    for row in rows:
        trends[row.brand].append(TrendPoint(date=row.date, score=row.score))
    return {brand: trends.get(brand, []) for brand in BRANDS}


def fetch_topic_distribution(db: Session) -> list[TopicDistributionItem]:
    """Return topic counts by brand."""

    rows = db.execute(
        select(Article.brand, Article.topic, func.count(Article.id))
        .group_by(Article.brand, Article.topic)
        .order_by(Article.brand, Article.topic)
    ).all()
    return [TopicDistributionItem(brand=row[0], topic=row[1], count=int(row[2])) for row in rows]


def fetch_recent_headlines(db: Session, limit: int = 30) -> list[str]:
    """Return recent headlines for insights generation."""

    rows = db.execute(select(Article.headline).order_by(desc(Article.created_at)).limit(limit)).all()
    return [str(row[0]) for row in rows]


def compute_negative_alerts(db: Session, threshold: float = 0.3) -> list[AlertItem]:
    """Detect brands with elevated negative coverage in the last 24 hours."""

    since = datetime.now(UTC) - timedelta(hours=24)
    rows = db.execute(
        select(
            Article.brand,
            func.count(Article.id),
            func.sum(case((Article.sentiment == "Negative", 1), else_=0)),
        )
        .where(Article.created_at >= since)
        .group_by(Article.brand)
    ).all()

    alerts: list[AlertItem] = []
    for brand in BRANDS:
        total = 0
        negative = 0
        for row in rows:
            if row[0] == brand:
                total = int(row[1] or 0)
                negative = int(row[2] or 0)
                break
        ratio = round((negative / total), 2) if total else 0.0
        alerts.append(
            AlertItem(
                brand=brand,
                negative_ratio=ratio,
                negative_articles=negative,
                total_articles=total,
                triggered=total > 0 and ratio > threshold,
            )
        )
    return alerts
