"""FastAPI application for the tyre intelligence platform."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.routers import alerts, articles, insights, pipeline_status, summary, trends


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Tyre Industry Intelligence Platform", version="1.0.0")
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
