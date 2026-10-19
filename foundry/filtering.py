"""Pure filtering so the UI and the tests share one implementation."""
from __future__ import annotations

from .schemas import Category, Scenario


def apply_filters(
    scenarios: list[Scenario],
    categories: list[Category] | None = None,
    bands: list[str] | None = None,
    query: str = "",
    min_priority: int = 1,
) -> list[Scenario]:
    q = query.strip().lower()
    out = []
    for s in scenarios:
        if categories and s.category not in categories:
            continue
        if bands and s.band not in bands:
            continue
        if s.priority < min_priority:
            continue
        if q:
            haystack = " ".join([s.id, s.title, s.description, s.risk, s.suggested_fix, " ".join(s.steps)]).lower()
            if q not in haystack:
                continue
        out.append(s)
    return out
