"""OpenAI-powered sentiment classification."""

from __future__ import annotations

from openai import APIConnectionError, APIError, OpenAI, RateLimitError

from backend.services.openai_utils import extract_json_object


ALLOWED_SENTIMENTS = {"Positive", "Neutral", "Negative"}


class SentimentAnalysisError(RuntimeError):
    """Raised when sentiment classification fails."""


class SentimentClassifier:
    """Classify financial news sentiment."""

    def __init__(self, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def classify(self, headline: str) -> str:
        """Return Positive, Neutral, or Negative."""

        prompt = (
            "You are a financial news sentiment classifier.\n\n"
            "Return JSON:\n"
            '{\n"sentiment": "Positive|Neutral|Negative"\n}\n\n'
            f"Headline:\n{headline}"
        )

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                temperature=0,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "Return only valid JSON."},
                    {"role": "user", "content": prompt},
                ],
            )
        except RateLimitError as exc:
            raise SentimentAnalysisError("OpenAI rate limit reached.") from exc
        except (APIConnectionError, APIError) as exc:
            raise SentimentAnalysisError(f"OpenAI request failed: {exc}") from exc

        message = response.choices[0].message.content if response.choices else None
        if not message:
            raise SentimentAnalysisError("OpenAI returned an empty sentiment response.")

        payload = extract_json_object(message)
        sentiment = str(payload.get("sentiment", "")).strip().title()
        if sentiment not in ALLOWED_SENTIMENTS:
            raise SentimentAnalysisError(f"Invalid sentiment returned: {sentiment or 'empty'}")
        return sentiment
