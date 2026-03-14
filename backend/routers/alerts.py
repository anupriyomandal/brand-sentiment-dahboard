"""Alerts endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import AlertItem
from backend.services.alert_engine import get_alerts


router = APIRouter(tags=["alerts"])


@router.get("/alerts", response_model=list[AlertItem])
def list_alerts(db: Session = Depends(get_db)) -> list[AlertItem]:
    """Return negative news alerts."""

    return get_alerts(db)
