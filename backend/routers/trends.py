"""Trends endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import TrendsResponse
from backend.services.analytics import fetch_topic_distribution, fetch_trends


router = APIRouter(tags=["trends"])


@router.get("/trends", response_model=TrendsResponse)
def get_trends(db: Session = Depends(get_db)) -> TrendsResponse:
    """Return sentiment trend lines and topic distribution."""

    return TrendsResponse(sentiment=fetch_trends(db), topics=fetch_topic_distribution(db))
