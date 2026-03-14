"""Alert engine facade."""

from __future__ import annotations

from sqlalchemy.orm import Session

from backend.schemas import AlertItem
from backend.services.analytics import compute_negative_alerts


def get_alerts(db: Session) -> list[AlertItem]:
    """Return current negative sentiment alerts."""

    return compute_negative_alerts(db)
