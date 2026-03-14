"""Pipeline status endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from backend.database import get_db
from backend.models import PipelineRun
from backend.schemas import PipelineRunStatus


router = APIRouter(tags=["pipeline"])


@router.get("/pipeline-status", response_model=PipelineRunStatus)
def get_latest_pipeline_status(db: Session = Depends(get_db)) -> PipelineRunStatus:
    """Return the latest pipeline run with brand-wise progress."""

    run = db.execute(
        select(PipelineRun)
        .options(selectinload(PipelineRun.brand_progress))
        .order_by(PipelineRun.started_at.desc())
        .limit(1)
    ).scalar_one_or_none()

    if run is None:
        raise HTTPException(status_code=404, detail="No pipeline runs found.")

    run.brand_progress.sort(key=lambda item: item.brand)
    return PipelineRunStatus.model_validate(run, from_attributes=True)
