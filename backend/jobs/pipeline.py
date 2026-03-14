"""Hourly ingestion pipeline."""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.models import Article, DailySentiment, PipelineBrandProgress, PipelineRun
from backend.services.analytics import build_summary_from_articles
from backend.services.common import AnalysedArticle
from backend.services.news_fetcher import GoogleNewsFetcher
from backend.services.sentiment import SentimentClassifier
from backend.services.topics import TopicClassifier

logger = logging.getLogger(__name__)

def run_hourly_pipeline(db: Session, limit_per_brand: int = 100) -> list[AnalysedArticle]:
    """Fetch, classify, deduplicate, store, and recompute daily sentiment."""

    settings = get_settings()
    fetcher = GoogleNewsFetcher(settings)
    sentiment = SentimentClassifier(settings.openai_api_key, settings.openai_model)
    topics = TopicClassifier(settings.openai_api_key, settings.openai_model)

    run = PipelineRun(status="running", started_at=datetime.now(UTC))
    db.add(run)
    db.commit()
    db.refresh(run)

    try:
        fetched = fetcher.fetch_all_brands(limit=limit_per_brand)
        analysed: list[AnalysedArticle] = []

        for brand, brand_articles in fetched.items():
            progress = PipelineBrandProgress(
                run_id=run.id,
                brand=brand,
                fetched=len(brand_articles),
                processed=0,
                added=0,
                status="running",
                updated_at=datetime.now(UTC),
            )
            db.add(progress)
            run.total_fetched += len(brand_articles)
            db.commit()
            db.refresh(progress)

            logger.info("Pipeline run %s: %s fetched=%s", run.id, brand, len(brand_articles))

            for article in brand_articles:
                progress.processed += 1
                run.total_processed += 1

                exists = db.execute(select(Article.id).where(Article.url == article.url)).scalar_one_or_none()
                if exists:
                    progress.updated_at = datetime.now(UTC)
                    db.commit()
                    continue

                item = AnalysedArticle(
                    brand=article.brand,
                    headline=article.headline,
                    source=article.source,
                    url=article.url,
                    sentiment=sentiment.classify(article.headline),
                    topic=topics.classify(article.headline),
                    published_date=article.published_date,
                    created_at=datetime.now(UTC),
                )
                analysed.append(item)
                progress.added += 1
                run.total_added += 1

                db.add(
                    Article(
                        brand=item.brand,
                        headline=item.headline,
                        source=item.source,
                        url=item.url,
                        sentiment=item.sentiment,
                        topic=item.topic,
                        published_date=item.published_date,
                        created_at=item.created_at,
                    )
                )
                progress.updated_at = datetime.now(UTC)
                db.commit()

            progress.status = "completed"
            progress.updated_at = datetime.now(UTC)
            db.commit()
            logger.info(
                "Pipeline run %s: %s processed=%s added=%s",
                run.id,
                brand,
                progress.processed,
                progress.added,
            )

        recompute_daily_sentiment(db)
        run.status = "completed"
        run.finished_at = datetime.now(UTC)
        db.commit()
        logger.info(
            "Pipeline run %s completed: fetched=%s processed=%s added=%s",
            run.id,
            run.total_fetched,
            run.total_processed,
            run.total_added,
        )
        return analysed
    except Exception as exc:
        run.status = "failed"
        run.error_message = str(exc)
        run.finished_at = datetime.now(UTC)
        db.commit()
        logger.exception("Pipeline run %s failed.", run.id)
        raise


def recompute_daily_sentiment(db: Session) -> None:
    """Recompute daily aggregates from stored articles."""

    articles = db.execute(select(Article)).scalars().all()
    grouped: dict[tuple[str, object], list[AnalysedArticle]] = {}

    for article in articles:
        key = (article.brand, article.published_date)
        grouped.setdefault(key, []).append(
            AnalysedArticle(
                brand=article.brand,
                headline=article.headline,
                source=article.source,
                url=article.url,
                sentiment=article.sentiment,
                topic=article.topic,
                published_date=article.published_date,
                created_at=article.created_at,
            )
        )

    db.execute(delete(DailySentiment))
    for (brand, summary_date), rows in grouped.items():
        summary = build_summary_from_articles(rows)[brand]
        db.add(
            DailySentiment(
                brand=brand,
                date=summary_date,
                articles=int(summary["articles"]),
                positive=int(summary["positive"]),
                neutral=int(summary["neutral"]),
                negative=int(summary["negative"]),
                score=float(summary["score"]),
            )
        )

    db.commit()
