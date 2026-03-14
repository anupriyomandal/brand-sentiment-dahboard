"""Google News RSS integration."""

from __future__ import annotations

from datetime import UTC, date, datetime
from email.utils import parsedate_to_datetime
from urllib.parse import urlencode

import feedparser
import requests

from backend.config import BRAND_QUERIES, Settings
from backend.services.common import NewsArticle


class NewsFetchError(RuntimeError):
    """Raised when news headlines cannot be fetched."""


class GoogleNewsFetcher:
    """Fetch Google News RSS headlines for configured tyre brands."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def fetch_news(self, brand: str, query: str, limit: int = 100) -> list[NewsArticle]:
        """Fetch news for a single brand."""

        url = self._build_url(query)
        feed = self._load_feed(url, brand)

        if getattr(feed, "bozo", False) and not getattr(feed, "entries", []):
            exception = getattr(feed, "bozo_exception", "Unknown feed parsing error")
            raise NewsFetchError(f"Google News RSS parsing failed for {brand}: {exception}")

        articles: list[NewsArticle] = []
        for entry in feed.entries[:limit]:
            headline = str(getattr(entry, "title", "")).strip()
            if not headline:
                continue

            link = str(getattr(entry, "link", "")).strip()
            source = "Unknown"
            if "source" in entry and getattr(entry.source, "title", ""):
                source = str(entry.source.title).strip()

            published_date = self._parse_published_date(getattr(entry, "published", ""))
            articles.append(
                NewsArticle(
                    brand=brand,
                    headline=headline,
                    source=source,
                    url=link,
                    published_date=published_date,
                )
            )

        return articles

    def fetch_all_brands(self, limit: int) -> dict[str, list[NewsArticle]]:
        """Fetch news for all configured brands."""

        return {
            brand: self.fetch_news(brand=brand, query=query, limit=limit)
            for brand, query in BRAND_QUERIES.items()
        }

    def _load_feed(self, url: str, brand: str) -> feedparser.FeedParserDict:
        """Download the RSS feed before parsing."""

        try:
            response = requests.get(
                url,
                timeout=self._settings.request_timeout,
                headers={"User-Agent": "tyre_intelligence_platform/1.0"},
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise NewsFetchError(f"Failed to fetch Google News RSS for {brand}: {exc}") from exc

        return feedparser.parse(response.content)

    def _build_url(self, query: str) -> str:
        params = urlencode(
            {
                "q": query,
                "hl": "en-IN",
                "gl": "IN",
                "ceid": "IN:en",
            }
        )
        return f"{self._settings.google_news_rss_base_url}?{params}"

    @staticmethod
    def _parse_published_date(raw_value: str) -> date:
        if not raw_value:
            return datetime.now(UTC).date()
        try:
            return parsedate_to_datetime(raw_value).date()
        except (TypeError, ValueError):
            return datetime.now(UTC).date()
