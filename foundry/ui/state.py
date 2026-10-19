"""Session-state access in one place so no other module touches raw keys."""
from __future__ import annotations

import streamlit as st

from ..schemas import Run


def set_run(run: Run) -> None:
    st.session_state["run"] = run
    st.session_state["nonce"] = st.session_state.get("nonce", 0) + 1  # resets filter widgets


def get_run() -> Run | None:
    return st.session_state.get("run")


def clear_run() -> None:
    st.session_state.pop("run", None)


def nonce() -> int:
    return st.session_state.get("nonce", 0)
