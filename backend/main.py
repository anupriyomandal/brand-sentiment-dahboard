"""FastAPI application for the tyre intelligence platform."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func

from backend.database import Base, engine
from backend.database import SessionLocal
from backend.jobs.pipeline import run_hourly_pipeline
from backend.models import Article
from backend.routers import alerts, articles, insights, pipeline_status, summary, trends


Base.metadata.create_all(bind=engine)
logger = logging.getLogger(__name__)


def seed_if_database_empty() -> None:
    """Populate the database on first boot so deployments are not empty."""

    db = SessionLocal()
    try:
        article_count = int(db.execute(select(func.count()).select_from(Article)).scalar_one())
        if article_count > 0:
            logger.info("Skipping startup seed because %s articles already exist.", article_count)
            return

        logger.info("Database is empty. Running initial ingestion seed for up to 100 articles per brand.")
        ingested = run_hourly_pipeline(db, limit_per_brand=100)
        logger.info("Initial ingestion seed completed with %s new articles.", len(ingested))
    except Exception:
        logger.exception("Initial ingestion seed failed during startup.")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_: FastAPI):
    seed_if_database_empty()
    yield


app = FastAPI(title="Tyre Industry Intelligence Platform", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summary.router)
app.include_router(articles.router)
app.include_router(trends.router)
app.include_router(insights.router)
app.include_router(alerts.router)
app.include_router(pipeline_status.router)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    """Health endpoint."""

    return {"status": "ok"}
