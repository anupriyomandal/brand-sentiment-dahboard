"""Google News RSS integration for fetching brand-related headlines."""

from __future__ import annotations

from urllib.parse import urlencode

import feedparser
import requests

from config import BRAND_QUERIES, Settings
from models import NewsArticle


class NewsFetchError(RuntimeError):
    """Raised when news headlines cannot be fetched."""


class GoogleNewsClient:
    """Client for the Google News RSS search endpoint."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def fetch_news(self, brand: str, query: str, limit: int = 20) -> list[NewsArticle]:
        """Fetch article headlines for a brand from Google News RSS."""

        url = self._build_url(query)
        feed = self._load_feed(url, brand)

        if getattr(feed, "bozo", False) and not getattr(feed, "entries", []):
            exception = getattr(feed, "bozo_exception", "Unknown feed parsing error")
            raise NewsFetchError(f"Google News RSS parsing failed for {brand}: {exception}")

        articles: list[NewsArticle] = []
        for entry in feed.entries[:limit]:
            title = str(getattr(entry, "title", "")).strip()
            link = str(getattr(entry, "link", "")).strip()
            source = "Unknown"
            if "source" in entry and getattr(entry.source, "title", ""):
                source = str(entry.source.title).strip()

            if not title:
                continue

            articles.append(
                NewsArticle(
                    brand=brand,
                    title=title,
                    link=link,
                    source=source,
                )
            )

        return articles

    def fetch_all_brands(self, limit: int) -> dict[str, list[NewsArticle]]:
        """Fetch article headlines for all configured brands."""

        return {
            brand: self.fetch_news(brand=brand, query=query, limit=limit)
            for brand, query in BRAND_QUERIES.items()
        }

    def _load_feed(self, url: str, brand: str) -> feedparser.FeedParserDict:
        """Download the RSS feed and parse it."""

        try:
            response = requests.get(
                url,
                timeout=self._settings.request_timeout,
                headers={"User-Agent": "tyre_sentiment_cli/1.0"},
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise NewsFetchError(f"Failed to fetch Google News RSS for {brand}: {exc}") from exc

        return feedparser.parse(response.content)

    def _build_url(self, query: str) -> str:
        """Build the Google News RSS URL for a search query."""

        params = urlencode(
            {
                "q": query,
                "hl": "en-IN",
                "gl": "IN",
                "ceid": "IN:en",
            }
        )
        return f"{self._settings.google_news_rss_base_url}?{params}"
