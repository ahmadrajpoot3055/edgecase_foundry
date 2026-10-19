"""Step 2: read the description, name the parts, and surface assumptions before generating anything."""
from __future__ import annotations

import json

from pydantic import ValidationError

from .llm import GroqClient, LLMError
from .schemas import SystemAnalysis

SYSTEM = (
    "You are a senior software architect reviewing a system described in plain English. "
    "Return ONLY a JSON object. Be concrete and specific to this system; no generic filler."
)

SHAPE = {
    "summary": "two sentences: what the system does and who relies on it",
    "components": ["the main parts, e.g. card reader, API, database"],
    "actors": ["people or systems that interact with it"],
    "assumptions": ["things the description takes for granted but never states"],
    "constraints": ["rules, limits, or deadlines that are stated or clearly implied"],
    "ambiguities": ["questions the description leaves open that change how it should behave"],
}


def analyze(client: GroqClient, description: str) -> SystemAnalysis:
    prompt = (
        "System description:\n<<<\n" + description + "\n>>>\n\n"
        "Return JSON in exactly this shape (3 to 7 items per list):\n" + json.dumps(SHAPE, indent=2)
    )
    data = client.generate_json(SYSTEM, prompt, temperature=0.3)
    if isinstance(data, list):
        data = data[0] if data else {}
    try:
        return SystemAnalysis.model_validate(data)
    except ValidationError as exc:
        raise LLMError(f"The analysis response did not match the expected schema: {exc.error_count()} errors.") from exc
