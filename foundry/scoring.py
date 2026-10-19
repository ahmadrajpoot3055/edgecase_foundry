"""One rubric, one formula. The model proposes severity and likelihood; Python owns everything after that."""
from __future__ import annotations

from .schemas import Scenario

SEVERITY_RUBRIC = {
    5: "Data loss, security breach, or money or legal harm",
    4: "Wrong outcome that persists and nobody is told",
    3: "Wrong outcome the user can see and recover from",
    2: "Degraded experience with an obvious workaround",
    1: "Cosmetic or negligible",
}
LIKELIHOOD_RUBRIC = {
    5: "Happens daily in normal use",
    4: "Happens weekly",
    3: "Happens monthly or under moderate load",
    2: "Rare; needs unusual timing or conditions",
    1: "Needs deliberate abuse or freak conditions",
}
BANDS = ("Critical", "High", "Medium", "Low")


def priority(severity: int, likelihood: int) -> int:
    return severity * likelihood


def band(score_value: int) -> str:
    if score_value >= 20:
        return "Critical"
    if score_value >= 12:
        return "High"
    if score_value >= 6:
        return "Medium"
    return "Low"


def score(s: Scenario) -> Scenario:
    p = priority(s.severity, s.likelihood)
    return s.model_copy(update={"priority": p, "band": band(p)})


def rank_and_label(scenarios: list[Scenario]) -> list[Scenario]:
    """Sort by priority (then severity), then assign stable IDs EC-01, EC-02..."""
    ordered = sorted(scenarios, key=lambda s: (-s.priority, -s.severity, s.title.lower()))
    return [s.model_copy(update={"id": f"EC-{i:02d}"}) for i, s in enumerate(ordered, 1)]
