"""Insights endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.database import get_db
from backend.schemas import InsightsResponse
from backend.services.analytics import fetch_recent_headlines, fetch_summary
from backend.services.insights_generator import InsightsGenerator


router = APIRouter(tags=["insights"])


@router.get("/insights", response_model=InsightsResponse)
def get_insights(db: Session = Depends(get_db)) -> InsightsResponse:
    """Return AI-generated industry insights."""

    settings = get_settings()
    summary = fetch_summary(db)
    headlines = fetch_recent_headlines(db)
    context = "\n".join(
        [f"{item.brand}: articles={item.articles}, pos={item.positive}, neg={item.negative}, score={item.score}" for item in summary]
        + headlines
    )
    generator = InsightsGenerator(settings.openai_api_key, settings.openai_model)
    return InsightsResponse(insights=generator.generate(context))
