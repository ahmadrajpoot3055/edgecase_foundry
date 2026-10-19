"""Thin Groq wrapper: JSON-only responses, retry on rate limits, one clear error type."""
from __future__ import annotations

import json
import re
import time
from typing import Any

import groq
from groq import Groq


class LLMError(RuntimeError):
    """Raised with a message that is safe to show to the user."""


def parse_json(text: str | None) -> Any:
    if not text or not text.strip():
        raise ValueError("empty response")
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    return json.loads(cleaned)


class GroqClient:
    def __init__(self, api_key: str, model: str, sleep=time.sleep):
        if not api_key:
            raise LLMError("No Groq API key. Set GROQ_API_KEY in your .env file.")
        self.model = model
        self._client = Groq(api_key=api_key, timeout=90)
        self._sleep = sleep

    def generate_json(self, system: str, prompt: str, temperature: float = 0.7, attempts: int = 3) -> Any:
        # Groq's JSON mode requires the word "JSON" somewhere in the messages.
        if "json" not in system.lower():
            system += "\nRespond with a single valid JSON object only."
        last: Exception | None = None
        for attempt in range(attempts):
            try:
                resp = self._client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    temperature=temperature,
                )
                return parse_json(resp.choices[0].message.content)
            except groq.AuthenticationError as exc:
                raise LLMError("Groq rejected the API key (401). Check GROQ_API_KEY in .env.") from exc
            except groq.NotFoundError as exc:
                raise LLMError(
                    f"Groq model '{self.model}' is not available on your key. "
                    "Set GROQ_MODEL in .env, e.g. openai/gpt-oss-120b."
                ) from exc
            except groq.RateLimitError as exc:
                last = exc
                if attempt < attempts - 1:
                    self._sleep(3 * (attempt + 1))
            except (groq.APIConnectionError, groq.InternalServerError, groq.BadRequestError) as exc:
                # BadRequest covers "json_validate_failed" when the model emits broken JSON; a retry usually fixes it.
                last = exc
                if attempt < attempts - 1:
                    self._sleep(1)
            except (ValueError, json.JSONDecodeError) as exc:
                last = exc
                if attempt < attempts - 1:
                    self._sleep(1)
        if isinstance(last, groq.RateLimitError):
            raise LLMError("Groq rate limit reached. Wait about a minute and generate again.") from last
        raise LLMError(f"Groq did not return usable JSON after {attempts} attempts: {last}") from last
