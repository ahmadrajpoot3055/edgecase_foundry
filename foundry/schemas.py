"""Pydantic models. Everything the LLM returns must pass through these before it reaches the UI."""
from __future__ import annotations

import re
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _norm(value: object) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


class Category(str, Enum):
    INVALID_INPUT = "Invalid input"
    BOUNDARY = "Boundary value"
    NETWORK = "Network failure"
    DUPLICATE = "Duplicate request"
    CONCURRENCY = "Concurrency"
    STATE = "State and timing"
    SECURITY = "Security and abuse"
    DATA = "Data integrity"
    USER = "User behavior"
    ENVIRONMENT = "Environment and scale"

    @classmethod
    def coerce(cls, value: object) -> "Category":
        if isinstance(value, cls):
            return value
        key = _norm(value).replace("and", "")
        for member in cls:
            if key in (_norm(member.value).replace("and", ""), _norm(member.name)):
                return member
        raise ValueError(f"unknown category: {value!r}")


class SystemAnalysis(BaseModel):
    model_config = ConfigDict(extra="ignore")

    summary: str = ""
    components: list[str] = Field(default_factory=list)
    actors: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    ambiguities: list[str] = Field(default_factory=list)

    @field_validator("components", "actors", "assumptions", "constraints", "ambiguities", mode="before")
    @classmethod
    def _clean_list(cls, v: object) -> list[str]:
        if v is None:
            return []
        if isinstance(v, str):
            v = [v]
        return [str(x).strip() for x in v if str(x).strip()]


class Scenario(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = ""
    title: str = Field(min_length=3, max_length=160)
    category: Category
    description: str = Field(min_length=10)
    risk: str = Field(min_length=5)
    severity: int = Field(ge=1, le=5)
    likelihood: int = Field(ge=1, le=5)
    input_conditions: str = Field(min_length=3)
    steps: list[str] = Field(min_length=2)
    expected_result: str = Field(min_length=3)
    pass_criteria: str = Field(min_length=3)
    fail_criteria: str = Field(min_length=3)
    suggested_fix: str = Field(min_length=3)
    # Filled by foundry.scoring, never by the model.
    priority: int = 0
    band: str = ""

    @field_validator("category", mode="before")
    @classmethod
    def _category(cls, v: object) -> Category:
        return Category.coerce(v)

    @field_validator("severity", "likelihood", mode="before")
    @classmethod
    def _clamp(cls, v: object) -> int:
        return max(1, min(5, int(round(float(v)))))

    @field_validator("steps", mode="before")
    @classmethod
    def _steps(cls, v: object) -> list[str]:
        if isinstance(v, str):
            v = re.split(r"\n+", v)
        cleaned = [re.sub(r"^\s*(\d+[.)]|[-*])\s*", "", str(s)).strip() for s in v]  # type: ignore[union-attr]
        return [s for s in cleaned if s]


class Stats(BaseModel):
    requested: int
    generated: int
    rejected: int
    duplicates_removed: int


class Run(BaseModel):
    id: int | None = None
    created_at: str
    description: str
    model: str
    analysis: SystemAnalysis
    scenarios: list[Scenario]
    stats: Stats
