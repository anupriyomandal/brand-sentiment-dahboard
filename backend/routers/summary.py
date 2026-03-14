"""Summary endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import SummaryItem
from backend.services.analytics import fetch_summary


router = APIRouter(tags=["summary"])


@router.get("/summary", response_model=list[SummaryItem])
def get_summary(db: Session = Depends(get_db)) -> list[SummaryItem]:
    """Return current brand sentiment summary."""

    return fetch_summary(db)
