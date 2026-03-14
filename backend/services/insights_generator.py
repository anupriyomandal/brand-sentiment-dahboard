"""AI-generated market insights."""

from __future__ import annotations

from openai import APIConnectionError, APIError, OpenAI, RateLimitError

from backend.services.openai_utils import extract_json_array


class InsightsGenerationError(RuntimeError):
    """Raised when insights generation fails."""


class InsightsGenerator:
    """Generate market insights from article and trend context."""

    def __init__(self, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def generate(self, context: str) -> list[str]:
        """Generate three concise insights."""

        prompt = (
            "You are a market analyst.\n\n"
            "Based on sentiment data and headlines,\n"
            "generate 3 insights about the tyre industry.\n\n"
            "Output format:\n"
            '[\n "Insight 1",\n "Insight 2",\n "Insight 3"\n]\n\n'
            f"Context:\n{context}"
        )

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                temperature=0.3,
                messages=[
                    {"role": "system", "content": "Return only a valid JSON array of strings."},
                    {"role": "user", "content": prompt},
                ],
            )
        except RateLimitError as exc:
            raise InsightsGenerationError("OpenAI rate limit reached.") from exc
        except (APIConnectionError, APIError) as exc:
            raise InsightsGenerationError(f"OpenAI request failed: {exc}") from exc

        message = response.choices[0].message.content if response.choices else None
        if not message:
            raise InsightsGenerationError("OpenAI returned an empty insights response.")

        insights = extract_json_array(message)
        return insights[:3]
