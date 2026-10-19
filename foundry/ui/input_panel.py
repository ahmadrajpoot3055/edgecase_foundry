"""Step 1: describe the system. Returns what the user asked for; does no generation itself."""
from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from .. import config
from ..schemas import Category
from . import components

SAMPLES = {
    "University attendance": (
        "Create a university attendance system where students scan their ID cards to mark attendance. "
        "A lecturer opens a session for each class, and attendance closes 15 minutes after the class starts. "
        "Cards are issued by the registrar and expire at the end of each academic year. Scans go to a central "
        "server over campus Wi-Fi, and lecturers can correct records for 48 hours afterwards."
    ),
    "Checkout and payments": (
        "An online store checkout. Customers add items to a cart, apply one discount code, enter a shipping "
        "address, and pay by card through a third-party payment provider. Stock is reserved while the customer "
        "pays and released after 10 minutes. Orders over 500 dollars need a manual fraud review before shipping."
    ),
    "Ride dispatch": (
        "A ride-hailing dispatcher. Riders request a trip, the system offers it to the nearest available driver "
        "who has 15 seconds to accept, then widens the search radius. Fares are calculated from distance, time, "
        "and a surge multiplier. Riders and drivers can cancel, with a fee after 2 minutes."
    ),
    "Clinic appointments": (
        "A clinic appointment booking app. Patients pick a doctor and a 20-minute slot, receive an SMS reminder "
        "24 hours before, and can reschedule up to 2 hours ahead. Doctors can block out time. Reception staff "
        "can double-book urgent cases. All times are shown in the clinic's local time zone."
    ),
}


@dataclass(frozen=True)
class Request:
    submitted: bool
    description: str
    count: int
    focus: list[Category]


def _load_sample(name: str) -> None:
    st.session_state["description"] = SAMPLES[name]


def render() -> Request:
    st.session_state.setdefault("description", "")
    st.text_area(
        "What does the system do, and what are its rules?",
        key="description", height=230, max_chars=config.MAX_DESCRIPTION_CHARS,
        placeholder="Example: A university attendance system where students scan their ID cards to mark attendance...",
        help="Include the rules, limits, and deadlines you know about. The more specific you are, the sharper the scenarios.",
    )
    text = st.session_state["description"].strip()
    short = len(text) < config.MIN_DESCRIPTION_CHARS
    components.render(
        f'<div class="counter{" bad" if short and text else ""}">{len(text)} of {config.MAX_DESCRIPTION_CHARS} characters'
        f'{"; add a little more detail to enable generation" if short else ""}</div>'
    )

    components.render('<div class="sample-note">Or start from a sample:</div>')
    names = list(SAMPLES)
    for row in range(0, len(names), 2):
        cols = st.columns(2)
        for col, name in zip(cols, names[row:row + 2]):
            col.button(name, key=f"sample_{name}", on_click=_load_sample, args=(name,), use_container_width=True)

    c1, c2 = st.columns([1, 1], gap="large")
    count = c1.slider("Scenarios per run", config.MIN_SCENARIOS, config.MAX_SCENARIOS, config.DEFAULT_SCENARIOS,
                      help="More scenarios take longer and use more of your free-tier quota.")
    focus = c2.multiselect("Focus on (leave empty for a broad spread)", [c.value for c in Category],
                           placeholder="All categories")
    submitted = st.button("Generate edge cases", type="primary", use_container_width=True, disabled=short)
    return Request(submitted, text, count, [Category.coerce(f) for f in focus])
