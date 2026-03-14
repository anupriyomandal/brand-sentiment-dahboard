"""Command-line entrypoint for the ingestion pipeline."""

from __future__ import annotations

from sqlalchemy import select, func

from backend.database import SessionLocal
from backend.jobs.pipeline import run_hourly_pipeline
from backend.models import Article


def main() -> None:
    """Run one ingestion cycle and print a compact summary."""

    db = SessionLocal()
    try:
        before = int(db.execute(select(func.count()).select_from(Article)).scalar_one())
        ingested = run_hourly_pipeline(db, limit_per_brand=100)
        after = int(db.execute(select(func.count()).select_from(Article)).scalar_one())
        print({"before": before, "added": len(ingested), "after": after})
    finally:
        db.close()


if __name__ == "__main__":
    main()
