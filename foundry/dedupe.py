"""Drop near-duplicate scenarios, keeping the higher-priority one."""
from __future__ import annotations

import re
from difflib import SequenceMatcher

from .schemas import Scenario

_STOP = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "at", "is", "are", "for", "with",
    "by", "from", "that", "this", "it", "as", "be", "when", "while", "same", "user", "system",
}


def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in _STOP and len(t) > 2}


def similarity(a: Scenario, b: Scenario) -> float:
    ta, tb = _tokens(f"{a.title} {a.description}"), _tokens(f"{b.title} {b.description}")
    jaccard = len(ta & tb) / len(ta | tb) if ta | tb else 0.0
    title_ratio = SequenceMatcher(None, a.title.lower(), b.title.lower()).ratio()
    return max(jaccard, title_ratio * 0.9)


def dedupe(scenarios: list[Scenario], threshold: float = 0.6) -> tuple[list[Scenario], int]:
    """Return (unique scenarios, number removed). Input must already be scored."""
    ranked = sorted(scenarios, key=lambda s: (-s.priority, -s.severity))
    kept: list[Scenario] = []
    for candidate in ranked:
        if all(similarity(candidate, k) < threshold for k in kept):
            kept.append(candidate)
    return kept, len(scenarios) - len(kept)
