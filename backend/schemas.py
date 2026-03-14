"""Pydantic schemas for API responses."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class SummaryItem(BaseModel):
    brand: str
    articles: int
    positive: int
    neutral: int
    negative: int
    score: float


class ArticleItem(BaseModel):
    id: int
    brand: str
    headline: str
    source: str
    url: str
    sentiment: str
    topic: str
    published_date: date
    created_at: datetime

    model_config = {"from_attributes": True}


class PaginatedArticles(BaseModel):
    page: int
    limit: int
    total: int
    items: list[ArticleItem]


class TrendPoint(BaseModel):
    date: date
    score: float


class TopicDistributionItem(BaseModel):
    brand: str
    topic: str
    count: int


class TrendsResponse(BaseModel):
    sentiment: dict[str, list[TrendPoint]]
    topics: list[TopicDistributionItem]


class InsightsResponse(BaseModel):
    insights: list[str] = Field(default_factory=list)


class AlertItem(BaseModel):
    brand: str
    negative_ratio: float
    negative_articles: int
    total_articles: int
    triggered: bool


class PipelineBrandProgressItem(BaseModel):
    brand: str
    fetched: int
    processed: int
    added: int
    status: str
    updated_at: datetime

    model_config = {"from_attributes": True}


class PipelineRunStatus(BaseModel):
    id: int
    status: str
    total_fetched: int
    total_processed: int
    total_added: int
    error_message: str | None
    started_at: datetime
    finished_at: datetime | None
    brand_progress: list[PipelineBrandProgressItem] = Field(default_factory=list)
