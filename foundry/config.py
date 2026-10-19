"""Runtime configuration. No Streamlit imports at module load so the core stays testable."""
from __future__ import annotations

import os
from pathlib import Path

DB_PATH = Path(os.getenv("EDGECASE_DB", "data/foundry.db"))
FALLBACK_MODEL = "openai/gpt-oss-120b"

MIN_SCENARIOS = 10
MAX_SCENARIOS = 20
DEFAULT_SCENARIOS = 12
OVERSAMPLE = 4  # ask the model for extras so de-duplication doesn't leave us short
MIN_DESCRIPTION_CHARS = 25
MAX_DESCRIPTION_CHARS = 4000

_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def _dotenv() -> dict[str, str]:
    """Read .env fresh on each call so edits apply without restarting Streamlit. Skipped under pytest."""
    if os.getenv("PYTEST_CURRENT_TEST") or not _ENV_FILE.is_file():
        return {}
    out: dict[str, str] = {}
    try:
        for line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return out


def _lookup(name: str) -> str:
    """Streamlit secrets, then process env, then .env."""
    if not os.getenv("PYTEST_CURRENT_TEST"):
        try:
            import streamlit as st

            if name in st.secrets and str(st.secrets[name]).strip():
                return str(st.secrets[name]).strip()
        except Exception:  # no secrets file, or running outside Streamlit
            pass
    return (os.getenv(name) or _dotenv().get(name) or "").strip()


def env_api_key() -> str:
    return _lookup("GROQ_API_KEY")


def model() -> str:
    return _lookup("GROQ_MODEL") or FALLBACK_MODEL


DEFAULT_MODEL = FALLBACK_MODEL  # kept for imports; use model() for the live value
