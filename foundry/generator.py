"""Step 3: ask the model for scenarios, then validate each one on its own so one bad item never sinks the batch."""
from __future__ import annotations

import json

from pydantic import ValidationError

from .llm import GroqClient, LLMError
from .schemas import Category, Scenario, SystemAnalysis
from .scoring import LIKELIHOOD_RUBRIC, SEVERITY_RUBRIC

SHAPE = {
    "scenarios": [
        {
            "title": "short, specific name",
            "category": "one of the allowed categories, spelled exactly",
            "description": "what happens, with concrete values and timings",
            "risk": "what goes wrong for the business or user if this is mishandled",
            "severity": "integer 1-5 using the severity rubric",
            "likelihood": "integer 1-5 using the likelihood rubric",
            "input_conditions": "exact starting state and inputs needed to reproduce",
            "steps": ["3 to 6 executable actions, one per item"],
            "expected_result": "what a correct system does",
            "pass_criteria": "observable check that proves it handled the case",
            "fail_criteria": "observable behavior that proves it did not",
            "suggested_fix": "one concrete change to the design or code",
        }
    ]
}

SYSTEM = (
    "You are a principal reliability engineer who breaks systems for a living. "
    "You find the situations developers overlook. Return ONLY a JSON object, no prose."
)


def build_prompt(description: str, analysis: SystemAnalysis, count: int, focus: list[Category]) -> str:
    cats = ", ".join(c.value for c in Category)
    focus_line = (
        f"Weight the set toward these categories: {', '.join(c.value for c in focus)}."
        if focus
        else "Spread scenarios across at least six different categories."
    )
    sev = "\n".join(f"  {k}: {v}" for k, v in sorted(SEVERITY_RUBRIC.items(), reverse=True))
    lik = "\n".join(f"  {k}: {v}" for k, v in sorted(LIKELIHOOD_RUBRIC.items(), reverse=True))
    return (
        f"System description:\n<<<\n{description}\n>>>\n\n"
        f"Analysis of the system:\n{analysis.model_dump_json(indent=2)}\n\n"
        f"Generate exactly {count} edge-case scenarios.\n"
        f"Allowed categories (use these exact strings): {cats}.\n{focus_line}\n\n"
        "Rules:\n"
        "- Every scenario must be specific to THIS system. Name its components and use concrete values "
        "(seconds, counts, IDs, sizes). Reject anything that would fit any system.\n"
        "- Each scenario is a distinct failure mode. Do not restate one with different wording.\n"
        "- Steps must be actions a tester can run, in order. Pass and fail criteria must be observable.\n"
        "- Include scenarios that probe the assumptions and ambiguities listed above.\n\n"
        f"Severity rubric:\n{sev}\nLikelihood rubric:\n{lik}\n\n"
        "Return JSON in exactly this shape:\n" + json.dumps(SHAPE, indent=2)
    )


def generate(
    client: GroqClient,
    description: str,
    analysis: SystemAnalysis,
    count: int,
    focus: list[Category] | None = None,
) -> tuple[list[Scenario], int]:
    """Return (valid scenarios, number of items rejected by validation)."""
    data = client.generate_json(SYSTEM, build_prompt(description, analysis, count, focus or []), temperature=0.8)
    items = data.get("scenarios") if isinstance(data, dict) else data
    if not isinstance(items, list):
        raise LLMError("The model response had no 'scenarios' list.")
    valid: list[Scenario] = []
    rejected = 0
    for item in items:
        try:
            valid.append(Scenario.model_validate(item))
        except (ValidationError, ValueError, TypeError):
            rejected += 1
    if not valid:
        raise LLMError("Every generated scenario failed validation. Try again or simplify the description.")
    return valid, rejected
