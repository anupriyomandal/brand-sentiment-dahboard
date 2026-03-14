"""Helpers for parsing OpenAI responses."""

from __future__ import annotations

import json


def extract_json_object(text: str) -> dict[str, object]:
    """Extract the first JSON object from a response body."""

    candidate = text.strip()
    if candidate.startswith("```"):
        lines = [line for line in candidate.splitlines() if not line.strip().startswith("```")]
        candidate = "\n".join(lines).strip()

    start = candidate.find("{")
    end = candidate.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in model response.")

    return json.loads(candidate[start : end + 1])


def extract_json_array(text: str) -> list[str]:
    """Extract a JSON array of strings from a response body."""

    candidate = text.strip()
    if candidate.startswith("```"):
        lines = [line for line in candidate.splitlines() if not line.strip().startswith("```")]
        candidate = "\n".join(lines).strip()

    start = candidate.find("[")
    end = candidate.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON array found in model response.")

    payload = json.loads(candidate[start : end + 1])
    return [str(item) for item in payload]
