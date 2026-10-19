"""Orchestrates the five steps: analyze, generate, validate, score, rank."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

from . import config, scoring
from .analyzer import analyze
from .dedupe import dedupe
from .generator import generate
from .llm import GroqClient, LLMError
from .schemas import Category, Run, Stats


def run_pipeline(
    client: GroqClient,
    description: str,
    count: int,
    focus: list[Category] | None = None,
    on_stage: Callable[[str], None] = lambda _msg: None,
) -> Run:
    description = description.strip()
    count = max(config.MIN_SCENARIOS, min(config.MAX_SCENARIOS, count))

    on_stage("Reading the description and listing assumptions")
    analysis = analyze(client, description)

    on_stage(f"Generating edge cases with {client.model}")
    candidates, rejected = generate(client, description, analysis, count + config.OVERSAMPLE, focus)

    on_stage("Scoring, removing duplicates, ranking")
    scored = [scoring.score(s) for s in candidates]
    unique, removed = dedupe(scored)
    ranked = scoring.rank_and_label(sorted(unique, key=lambda s: (-s.priority, -s.severity))[:count])
    if not ranked:
        raise LLMError("No scenarios survived validation.")

    return Run(
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        description=description,
        model=client.model,
        analysis=analysis,
        scenarios=ranked,
        stats=Stats(requested=count, generated=len(candidates), rejected=rejected, duplicates_removed=removed),
    )
