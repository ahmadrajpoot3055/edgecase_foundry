"""SQLite history. One table, whole run stored as validated JSON."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from . import config
from .schemas import Run

_SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    title TEXT NOT NULL,
    model TEXT NOT NULL,
    scenario_count INTEGER NOT NULL,
    payload TEXT NOT NULL
)
"""


@dataclass(frozen=True)
class RunSummary:
    id: int
    created_at: str
    title: str
    scenario_count: int


@contextmanager
def _conn(path: Path | None = None) -> Iterator[sqlite3.Connection]:
    db = Path(path or config.DB_PATH)
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db)
    try:
        yield con
        con.commit()
    finally:
        con.close()


def init_db(path: Path | None = None) -> None:
    with _conn(path) as con:
        con.execute(_SCHEMA)


def save_run(run: Run, path: Path | None = None) -> int:
    title = " ".join(run.description.split())[:70]
    with _conn(path) as con:
        cur = con.execute(
            "INSERT INTO runs (created_at, title, model, scenario_count, payload) VALUES (?, ?, ?, ?, ?)",
            (run.created_at, title, run.model, len(run.scenarios), run.model_dump_json()),
        )
        return int(cur.lastrowid)


def list_runs(limit: int = 25, path: Path | None = None) -> list[RunSummary]:
    with _conn(path) as con:
        rows = con.execute(
            "SELECT id, created_at, title, scenario_count FROM runs ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [RunSummary(*r) for r in rows]


def load_run(run_id: int, path: Path | None = None) -> Run | None:
    with _conn(path) as con:
        row = con.execute("SELECT payload FROM runs WHERE id = ?", (run_id,)).fetchone()
    if not row:
        return None
    run = Run.model_validate_json(row[0])
    return run.model_copy(update={"id": run_id})


def delete_run(run_id: int, path: Path | None = None) -> None:
    with _conn(path) as con:
        con.execute("DELETE FROM runs WHERE id = ?", (run_id,))
