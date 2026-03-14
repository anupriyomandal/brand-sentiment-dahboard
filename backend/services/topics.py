"""OpenAI-powered topic classification."""

from __future__ import annotations

from openai import APIConnectionError, APIError, OpenAI, RateLimitError

from backend.config import TOPICS
from backend.services.openai_utils import extract_json_object


class TopicClassificationError(RuntimeError):
    """Raised when topic classification fails."""


class TopicClassifier:
    """Classify tyre news into a controlled topic taxonomy."""

    def __init__(self, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def classify(self, headline: str) -> str:
        """Return one configured topic label."""

        topic_list = ", ".join(TOPICS)
        prompt = (
            "Classify the topic of this news headline.\n\n"
            f"Allowed topics: {topic_list}\n\n"
            "Return JSON:\n"
            '{\n"topic": "Product Launch|Earnings|Exports|Market Expansion|Cost Pressure|EV Tyres|Regulation|Other"\n}\n\n'
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
            raise TopicClassificationError("OpenAI rate limit reached.") from exc
        except (APIConnectionError, APIError) as exc:
            raise TopicClassificationError(f"OpenAI request failed: {exc}") from exc

        message = response.choices[0].message.content if response.choices else None
        if not message:
            raise TopicClassificationError("OpenAI returned an empty topic response.")

        payload = extract_json_object(message)
        topic = str(payload.get("topic", "")).strip()
        if topic not in TOPICS:
            return "Other"
        return topic
