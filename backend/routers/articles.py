"""Articles endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Article
from backend.schemas import PaginatedArticles


router = APIRouter(tags=["articles"])


@router.get("/articles", response_model=PaginatedArticles)
def get_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    brand: str | None = None,
    sentiment: str | None = None,
    topic: str | None = None,
    db: Session = Depends(get_db),
) -> PaginatedArticles:
    """Return paginated articles with optional filters."""

    query = select(Article).order_by(Article.created_at.desc())

    if brand:
        query = query.where(Article.brand == brand)
    if sentiment:
        query = query.where(Article.sentiment == sentiment)
    if topic:
        query = query.where(Article.topic == topic)

    count_query = select(func.count()).select_from(query.order_by(None).subquery())
    total = int(db.execute(count_query).scalar_one())
    items = db.execute(query.offset((page - 1) * limit).limit(limit)).scalars().all()
    return PaginatedArticles(page=page, limit=limit, total=total, items=items)
