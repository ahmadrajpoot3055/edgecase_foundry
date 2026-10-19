"""Steps 3 to 5 in the UI: risk map, filters, scenario ledger, exports."""
from __future__ import annotations

from datetime import datetime

import streamlit as st

from .. import exporters, scoring
from ..filtering import apply_filters
from ..schemas import Category, Run
from . import charts, components, state


def _plot(fig) -> None:
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _exports(run: Run, shown: list) -> tuple[bytes, bytes]:
    """Build CSV and PDF once per (run, visible set); reruns from unrelated clicks reuse them."""
    key = (run.id, run.created_at, tuple(s.id for s in shown))
    cache = st.session_state.get("_export_cache")
    if not cache or cache[0] != key:
        cache = (key, exporters.to_csv_bytes(shown), exporters.to_pdf_bytes(run, shown))
        st.session_state["_export_cache"] = cache
    return cache[1], cache[2]


def render(run: Run) -> None:
    n = state.nonce()
    components.section(2, "What the system is", "Read this first. A wrong assumption here produces wrong scenarios.")
    components.stats_strip(run)

    left, right = st.columns([4, 7], gap="large")
    with left:
        components.analysis_panel(run.analysis)
    with right:
        _plot(charts.risk_matrix(run.scenarios))
        a, b = st.columns([3, 2])
        with a:
            _plot(charts.category_chart(run.scenarios))
        with b:
            _plot(charts.severity_chart(run.scenarios))

    components.section(3, "Review and export", "Filters apply to the list and to both downloads.")
    f1, f2, f3, f4 = st.columns([3, 2, 3, 2], gap="medium")
    cats = f1.multiselect("Category", [c.value for c in Category if any(s.category == c for s in run.scenarios)],
                          key=f"f_cat_{n}", placeholder="All")
    bands = f2.multiselect("Priority band", list(scoring.BANDS), key=f"f_band_{n}", placeholder="All")
    query = f3.text_input("Search titles, steps, fixes", key=f"f_q_{n}")
    min_p = f4.slider("Minimum priority", 1, 25, 1, key=f"f_p_{n}")

    shown = apply_filters(run.scenarios, [Category.coerce(c) for c in cats], bands, query, min_p)

    info, d1, d2 = st.columns([5, 2, 2], gap="medium")
    info.markdown(f'<div class="shown">Showing {len(shown)} of {len(run.scenarios)} scenarios</div>', unsafe_allow_html=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    has = bool(shown)
    csv_bytes, pdf_bytes = _exports(run, shown) if has else (b"", b"")
    d1.download_button(
        "Download CSV", data=csv_bytes, file_name=f"edgecase-foundry-{stamp}.csv",
        mime="text/csv", disabled=not has, key=f"dl_csv_{n}", use_container_width=True,
    )
    d2.download_button(
        "Download PDF", data=pdf_bytes, file_name=f"edgecase-foundry-{stamp}.pdf",
        mime="application/pdf", disabled=not has, key=f"dl_pdf_{n}", use_container_width=True,
    )
    st.write("")
    components.ledger(shown)
