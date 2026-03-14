"""Utility helpers for text parsing."""

from __future__ import annotations

import json


def extract_json_object(text: str) -> dict[str, object]:
    """Extract the first JSON object from a model response."""

    candidate = text.strip()
    if candidate.startswith("```"):
        lines = [line for line in candidate.splitlines() if not line.strip().startswith("```")]
        candidate = "\n".join(lines).strip()

    start = candidate.find("{")
    end = candidate.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in model response.")

    return json.loads(candidate[start : end + 1])
