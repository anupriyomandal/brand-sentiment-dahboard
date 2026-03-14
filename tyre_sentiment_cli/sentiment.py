"""Sentiment analysis using the OpenAI API."""

from __future__ import annotations

from openai import APIConnectionError, APIError, OpenAI, RateLimitError

from models import ArticleResult, NewsArticle
from utils import extract_json_object


ALLOWED_SENTIMENTS = {"Positive", "Negative", "Neutral"}


class SentimentAnalysisError(RuntimeError):
    """Raised when sentiment classification fails."""


class SentimentClassifier:
    """Classify headline sentiment with an OpenAI chat model."""

    def __init__(self, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def classify_sentiment(self, headline: str) -> str:
        """Return Positive, Negative, or Neutral for a news headline."""

        prompt = (
            "You are a brand sentiment classifier.\n\n"
            "Classify the sentiment of this headline about a company.\n\n"
            "Return JSON:\n"
            '{\n"sentiment": "Positive | Negative | Neutral"\n}\n\n'
            "Allowed labels:\n"
            "Positive\n"
            "Negative\n"
            "Neutral\n\n"
            f"Headline:\n{headline}"
        )

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                temperature=0,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "You return only valid JSON for headline sentiment classification.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        except RateLimitError as exc:
            raise SentimentAnalysisError("OpenAI rate limit reached. Please retry later.") from exc
        except (APIConnectionError, APIError) as exc:
            raise SentimentAnalysisError(f"OpenAI request failed: {exc}") from exc

        message = response.choices[0].message.content if response.choices else None
        if not message:
            raise SentimentAnalysisError("OpenAI returned an empty classification response.")

        payload = extract_json_object(message)
        sentiment = str(payload.get("sentiment", "")).strip().title()
        if sentiment not in ALLOWED_SENTIMENTS:
            raise SentimentAnalysisError(f"Invalid sentiment returned by model: {sentiment or 'empty'}")

        return sentiment

    def analyse_articles(self, articles: list[NewsArticle]) -> list[ArticleResult]:
        """Classify a list of article headlines."""

        results: list[ArticleResult] = []
        for article in articles:
            sentiment = self.classify_sentiment(article.title)
            results.append(
                ArticleResult(
                    brand=article.brand,
                    title=article.title,
                    sentiment=sentiment,
                )
            )
        return results
