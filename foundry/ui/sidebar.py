"""Sidebar: Saved run history. Engine settings are configured via .env."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import streamlit as st

from .. import config, storage
from . import components, state


@dataclass(frozen=True)
class EngineConfig:
    api_key: str
    model: str


def _open(run_id: int) -> None:
    run = storage.load_run(run_id)
    if run:
        state.set_run(run)


def _delete(run_id: int) -> None:
    current = state.get_run()
    storage.delete_run(run_id)
    if current and current.id == run_id:
        state.clear_run()


def _when(iso: str) -> str:
    try:
        return datetime.fromisoformat(iso).astimezone().strftime("%d %b, %H:%M")
    except ValueError:
        return iso


def render() -> EngineConfig:
    api_key, model = config.env_api_key(), config.model()
    with st.sidebar:
        st.subheader("Saved Runs")
        runs = storage.list_runs()
        if not runs:
            st.caption("No runs yet. Each successful generation is saved here automatically.")
        for r in runs:
            components.render(
                f'<div class="hist"><b>{components.esc(r.title)}</b><br>'
                f'<span class="hist-meta">{_when(r.created_at)} • {r.scenario_count} scenarios</span></div>'
            )
            c1, c2 = st.columns(2)
            c1.button("Open", key=f"open_{r.id}", on_click=_open, args=(r.id,), use_container_width=True)
            c2.button("Delete", key=f"del_{r.id}", on_click=_delete, args=(r.id,), use_container_width=True)

        st.divider()
        status = "keystate" if api_key else "keystate-warn"
        label = f"Groq · {components.esc(model)}" if api_key else "GROQ_API_KEY missing in .env"
        components.render(f'<div class="{status}">{label}</div>')

    return EngineConfig(api_key=api_key, model=model)
