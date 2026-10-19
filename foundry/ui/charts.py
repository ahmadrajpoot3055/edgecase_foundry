"""Plotly figures styled in clean minimalism with Poppins typography."""
from __future__ import annotations

from collections import Counter

import plotly.graph_objects as go

from .. import scoring
from ..schemas import Scenario
from .theme import CRITICAL, HIGH, LOW, MEDIUM, POPPINS, PRIMARY, TEXT_DARK, TEXT_MUTED

_BAND_FILL = {
    "Critical": "rgba(239, 68, 68, 0.18)",
    "High": "rgba(249, 115, 22, 0.16)",
    "Medium": "rgba(245, 158, 11, 0.15)",
    "Low": "rgba(16, 185, 129, 0.13)",
}


def _base(fig: go.Figure, height: int, title: str) -> go.Figure:
    fig.update_layout(
        height=height,
        title=dict(
            text=title,
            x=0,
            font=dict(family=f"'{POPPINS}', sans-serif", size=14, color=TEXT_DARK, weight=600),
        ),
        margin=dict(l=10, r=16, t=44, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(family=f"'{POPPINS}', sans-serif", color=TEXT_DARK, size=11),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#0F172A",
            bordercolor="#0F172A",
            font=dict(family=f"'{POPPINS}', sans-serif", color="#FFFFFF", size=11),
        ),
    )
    return fig


def risk_matrix(scenarios: list[Scenario]) -> go.Figure:
    fig = go.Figure()
    for sev in range(1, 6):
        for lik in range(1, 6):
            fig.add_shape(
                type="rect",
                x0=lik - 0.5,
                x1=lik + 0.5,
                y0=sev - 0.5,
                y1=sev + 0.5,
                layer="below",
                fillcolor=_BAND_FILL[scoring.band(scoring.priority(sev, lik))],
                line=dict(color="#E2E8F0", width=1),
            )
    counts = Counter((s.severity, s.likelihood) for s in scenarios)
    xs = [lik for (_, lik) in counts]
    ys = [sev for (sev, _) in counts]
    ns = list(counts.values())
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="markers+text",
            text=[str(n) for n in ns],
            textfont=dict(color="#FFFFFF", size=12, family=f"'{POPPINS}', sans-serif", weight=700),
            marker=dict(
                size=[22 + 6 * n for n in ns],
                color=PRIMARY,
                line=dict(color="#FFFFFF", width=2),
                opacity=0.92,
            ),
            hovertemplate="Severity %{y}, Likelihood %{x}<br><b>%{text}</b> scenario(s)<extra></extra>",
        )
    )
    fig.update_xaxes(
        range=[0.5, 5.5],
        dtick=1,
        title="Likelihood (1: Rare → 5: Inevitable)",
        showgrid=False,
        zeroline=False,
        fixedrange=True,
        title_font=dict(color=TEXT_MUTED, size=11),
    )
    fig.update_yaxes(
        range=[0.5, 5.5],
        dtick=1,
        title="Severity (1: Cosmetic → 5: Critical)",
        showgrid=False,
        zeroline=False,
        fixedrange=True,
        title_font=dict(color=TEXT_MUTED, size=11),
    )
    return _base(fig, 360, "Risk Distribution Matrix")


def category_chart(scenarios: list[Scenario]) -> go.Figure:
    counts = Counter(s.category.value for s in scenarios)
    items = sorted(counts.items(), key=lambda kv: kv[1])
    fig = go.Figure(
        go.Bar(
            x=[v for _, v in items],
            y=[k for k, _ in items],
            orientation="h",
            marker=dict(color=PRIMARY, line=dict(color="#4338CA", width=1)),
            text=[v for _, v in items],
            textposition="outside",
            textfont=dict(family=f"'{POPPINS}', sans-serif", size=11, weight=600),
            cliponaxis=False,
            hovertemplate="%{y}: <b>%{x}</b><extra></extra>",
        )
    )
    fig.update_xaxes(showgrid=False, visible=False, fixedrange=True)
    fig.update_yaxes(
        fixedrange=True,
        automargin=True,
        tickfont=dict(family=f"'{POPPINS}', sans-serif", size=11, color=TEXT_DARK),
    )
    return _base(fig, max(240, 34 * len(items) + 70), "Scenarios by Category")


def severity_chart(scenarios: list[Scenario]) -> go.Figure:
    counts = Counter(s.severity for s in scenarios)
    levels = [1, 2, 3, 4, 5]
    colors = ["#CBD5E1", "#94A3B8", MEDIUM, HIGH, CRITICAL]
    fig = go.Figure(
        go.Bar(
            x=[f"Sev {l}" for l in levels],
            y=[counts.get(l, 0) for l in levels],
            marker=dict(color=colors, line=dict(color="rgba(0,0,0,0.05)", width=1)),
            text=[counts.get(l, 0) for l in levels],
            textposition="outside",
            textfont=dict(family=f"'{POPPINS}', sans-serif", size=11, weight=600),
            cliponaxis=False,
            hovertemplate="%{x}: <b>%{y}</b><extra></extra>",
        )
    )
    fig.update_yaxes(visible=False, showgrid=False, fixedrange=True)
    fig.update_xaxes(
        fixedrange=True,
        tickfont=dict(family=f"'{POPPINS}', sans-serif", size=11, color=TEXT_DARK),
    )
    return _base(fig, 280, "Severity Breakdown")
