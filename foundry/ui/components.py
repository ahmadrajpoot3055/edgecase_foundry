"""Stateless HTML builders. Every piece of model text goes through esc() before it touches markup.

Markdown rules these builders respect: no blank lines inside an HTML block, and `$` is escaped
so Streamlit does not try to typeset prices as LaTeX.
"""
from __future__ import annotations

import html

import streamlit as st

from .. import scoring
from ..schemas import Run, Scenario, SystemAnalysis


def esc(text: object) -> str:
    return html.escape(" ".join(str(text).split())).replace("$", "&#36;")


def render(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


def masthead() -> None:
    render(
        '<div class="mast"><div class="tape"></div>'
        '<div class="badge">⚡ Edge-Case & Boundary Testing</div>'
        '<h1 class="title"><span>EdgeCase</span><span>Foundry</span></h1>'
        '<p class="lede">Describe any architecture, user flow, or business rules in plain English. '
        'Automatically generate high-risk edge cases, corner conditions, and test execution procedures.</p>'
        '<div class="stamp">🎯 Generates test scenarios to execute • Verify against your implementation</div></div>'
    )


def section(num: int, title: str, hint: str = "") -> None:
    hint_html = f'<div class="h">{esc(hint)}</div>' if hint else ""
    render(f'<div class="sec"><div class="n">0{num}</div><div class="t">{esc(title)}</div>{hint_html}</div>')


def rubric_panel() -> None:
    rows = "".join(
        f'<tr><td class="lv">{lvl}</td><td>{esc(scoring.SEVERITY_RUBRIC[lvl])}</td>'
        f'<td>{esc(scoring.LIKELIHOOD_RUBRIC[lvl])}</td></tr>'
        for lvl in (5, 4, 3, 2, 1)
    )
    render(
        '<div class="rubric"><h3>Scoring Rubric & Risk Bands</h3>'
        '<div class="formula">Priority = Severity × Likelihood (Range: 1 to 25)</div>'
        f'<table><tr><th>Lvl</th><th>Severity</th><th>Likelihood</th></tr>{rows}</table>'
        '<div class="bands"><span class="b-critical">Critical 20–25</span><span class="b-high">High 12–19</span>'
        '<span class="b-medium">Medium 6–11</span><span class="b-low">Low 1–5</span></div></div>'
    )


def stats_strip(run: Run) -> None:
    by_band = {b: sum(1 for s in run.scenarios if s.band == b) for b in scoring.BANDS}
    avg = sum(s.priority for s in run.scenarios) / len(run.scenarios)
    cells = (
        f'<div class="c wide"><b>{len(run.scenarios)}</b>Total Scenarios ({esc(run.model)})</div>'
        f'<div class="c b-critical"><b>{by_band["Critical"]}</b>Critical</div>'
        f'<div class="c b-high"><b>{by_band["High"]}</b>High</div>'
        f'<div class="c b-medium"><b>{by_band["Medium"]}</b>Medium</div>'
        f'<div class="c b-low"><b>{by_band["Low"]}</b>Low</div>'
        f'<div class="c"><b>{avg:.1f}</b>Avg Priority</div>'
        f'<div class="c"><b>{run.stats.duplicates_removed}</b>Deduped</div>'
        f'<div class="c"><b>{run.stats.rejected}</b>Filtered</div>'
    )
    render(f'<div class="strip">{cells}</div>')


def _ul(items: list[str], cls: str = "") -> str:
    return f'<ul class="{cls}">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def analysis_panel(a: SystemAnalysis) -> None:
    parts = [f'<p class="sum">{esc(a.summary)}</p>'] if a.summary else []
    for title, items, cls in [
        ("Components", a.components, ""),
        ("Actors & Interactors", a.actors, ""),
        ("System Assumptions", a.assumptions, ""),
        ("Constraints", a.constraints, ""),
        ("Open Questions & Ambiguities", a.ambiguities, "q"),
    ]:
        if items:
            parts.append(f"<h4>{esc(title)}</h4>{_ul(items, cls)}")
    render(f'<div class="brief">{"".join(parts)}</div>')


def _case(s: Scenario, is_open: bool) -> str:
    steps = "".join(f"<li>{esc(x)}</li>" for x in s.steps)
    return (
        f'<details class="case"{" open" if is_open else ""}><summary>'
        f'<span class="id">{esc(s.id)}</span>'
        f'<span class="sc b-{s.band.lower()}" title="{esc(s.band)}">{s.priority}</span>'
        f'<span class="ttl">{esc(s.title)}</span>'
        f'<span class="cat">{esc(s.category.value)}</span>'
        f'<span class="sl">S{s.severity} × L{s.likelihood}</span></summary>'
        '<div class="body"><div class="col">'
        f'<h5>What Happens</h5><p>{esc(s.description)}</p>'
        f'<h5>Why It Matters (Risk)</h5><p>{esc(s.risk)}</p>'
        f'<h5>Preconditions & Setup</h5><p>{esc(s.input_conditions)}</p>'
        f'<h5>Suggested Fix</h5><p>{esc(s.suggested_fix)}</p></div>'
        '<div class="col">'
        f'<h5>Test Steps</h5><ol>{steps}</ol>'
        f'<h5>Expected Result</h5><p>{esc(s.expected_result)}</p>'
        f'<div class="pass"><b>Pass Condition</b>{esc(s.pass_criteria)}</div>'
        f'<div class="fail"><b>Fail Condition</b>{esc(s.fail_criteria)}</div></div></div></details>'
    )


def ledger(scenarios: list[Scenario]) -> None:
    if not scenarios:
        render('<div class="empty">No scenarios match the selected filters. Loosen your filter criteria above.</div>')
        return
    render("".join(_case(s, i == 0) for i, s in enumerate(scenarios)))


def empty_state() -> None:
    render(
        '<div class="empty" style="margin-top:1.5rem">No scenarios generated yet. '
        'Describe your system above, or click one of the quick samples, then click <b>Generate edge cases</b>. '
        'Saved runs are accessible anytime in the sidebar.</div>'
    )
