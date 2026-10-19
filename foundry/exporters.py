"""CSV and PDF export. Both take the (possibly filtered) scenario list the user is looking at."""
from __future__ import annotations

import io
from datetime import datetime
from xml.sax.saxutils import escape

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .schemas import Run, Scenario
from .scoring import BANDS

INK = colors.HexColor("#000000")
CONCRETE = colors.HexColor("#D4D3CC")
HAZARD = colors.HexColor("#FFD500")
FAIL = colors.HexColor("#E0241B")
WHITE = colors.white
BAND_BG = {"Critical": FAIL, "High": INK, "Medium": HAZARD, "Low": CONCRETE}
BAND_FG = {"Critical": WHITE, "High": HAZARD, "Medium": INK, "Low": INK}

COLUMNS = [
    "id", "title", "category", "severity", "likelihood", "priority", "band", "description", "risk",
    "input_conditions", "steps", "expected_result", "pass_criteria", "fail_criteria", "suggested_fix",
]


def _csv_safe(value: object) -> object:
    """Neutralise spreadsheet formula injection from model-generated text."""
    if isinstance(value, str) and value[:1] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + value
    return value


def scenarios_to_df(scenarios: list[Scenario]) -> pd.DataFrame:
    rows = []
    for s in scenarios:
        d = s.model_dump()
        d["category"] = s.category.value
        d["steps"] = "\n".join(f"{i}. {step}" for i, step in enumerate(s.steps, 1))
        rows.append({c: d[c] for c in COLUMNS})
    return pd.DataFrame(rows, columns=COLUMNS)


def to_csv_bytes(scenarios: list[Scenario]) -> bytes:
    df = scenarios_to_df(scenarios).apply(lambda col: col.map(_csv_safe))
    return df.to_csv(index=False).encode("utf-8-sig")  # BOM so Excel reads UTF-8


# ---------- PDF ----------

def _t(text: str) -> str:
    """Make text safe for ReportLab's built-in fonts (cp1252) and for its XML-ish Paragraph parser."""
    return escape(text.encode("cp1252", "replace").decode("cp1252"))


def _styles() -> dict[str, ParagraphStyle]:
    return {
        "title": ParagraphStyle("title", fontName="Times-Bold", fontSize=40, leading=36, textColor=INK),
        "sub": ParagraphStyle("sub", fontName="Courier-Bold", fontSize=9, leading=12, textColor=INK),
        "body": ParagraphStyle("body", fontName="Courier", fontSize=8, leading=11, textColor=INK),
        "label": ParagraphStyle("label", fontName="Courier-Bold", fontSize=8, leading=11, textColor=INK),
        "h2": ParagraphStyle("h2", fontName="Times-Bold", fontSize=18, leading=20, spaceBefore=10, spaceAfter=4),
        "cell": ParagraphStyle("cell", fontName="Courier", fontSize=7.5, leading=9.5, textColor=INK),
        "cellb": ParagraphStyle("cellb", fontName="Courier-Bold", fontSize=7.5, leading=9.5, textColor=INK),
    }


def _footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Courier", 7)
    canvas.setFillColor(INK)
    canvas.drawString(15 * mm, 9 * mm, "EdgeCase Foundry. Generated scenarios to be tested, not verified results.")
    canvas.drawRightString(195 * mm, 9 * mm, f"Page {doc.page}")
    canvas.setFillColor(HAZARD)
    canvas.rect(15 * mm, 12 * mm, 180 * mm, 1.6 * mm, stroke=0, fill=1)
    canvas.restoreState()


def _scenario_block(s: Scenario, st: dict[str, ParagraphStyle]) -> KeepTogether:
    head_style = ParagraphStyle("hd", parent=st["cellb"], textColor=WHITE, fontSize=8.5, leading=11)
    band_style = ParagraphStyle(
        "bd", parent=st["cellb"], textColor=BAND_FG[s.band], alignment=1, fontSize=8.5, leading=11
    )
    rows: list[list] = [
        [
            Paragraph(_t(s.id), head_style),
            Paragraph(_t(s.title), head_style),
            Paragraph(f"P{s.priority} {_t(s.band)}", band_style),
        ]
    ]
    steps = [Paragraph(f"{i}. {_t(step)}", st["cell"]) for i, step in enumerate(s.steps, 1)]
    detail = [
        ("Category", s.category.value + f"  (severity {s.severity} x likelihood {s.likelihood})"),
        ("Scenario", s.description),
        ("Risk", s.risk),
        ("Input conditions", s.input_conditions),
        ("Steps", steps),
        ("Expected result", s.expected_result),
        ("Pass when", s.pass_criteria),
        ("Fail when", s.fail_criteria),
        ("Suggested fix", s.suggested_fix),
    ]
    for label, value in detail:
        cell = value if isinstance(value, list) else Paragraph(_t(value), st["cell"])
        rows.append([Paragraph(label, st["cellb"]), cell, ""])
    table = Table(rows, colWidths=[34 * mm, 116 * mm, 30 * mm])
    style = [
        ("BACKGROUND", (0, 0), (1, 0), INK),
        ("BACKGROUND", (2, 0), (2, 0), BAND_BG[s.band]),
        ("BOX", (0, 0), (-1, -1), 1.6, INK),
        ("LINEBELOW", (0, 1), (-1, -2), 0.4, CONCRETE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    style += [("SPAN", (1, r), (2, r)) for r in range(1, len(rows))]
    table.setStyle(TableStyle(style))
    return KeepTogether([table, Spacer(1, 5 * mm)])


def to_pdf_bytes(run: Run, scenarios: list[Scenario]) -> bytes:
    st = _styles()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=15 * mm, bottomMargin=18 * mm,
        title="EdgeCase Foundry report", author="EdgeCase Foundry",
    )
    story: list = [
        Paragraph("EdgeCase<br/>Foundry", st["title"]),
        Spacer(1, 3 * mm),
        Paragraph(
            _t(f"Report generated {datetime.now().strftime('%d %b %Y %H:%M')} with {run.model}. "
               f"{len(scenarios)} of {len(run.scenarios)} scenarios included."),
            st["sub"],
        ),
        Spacer(1, 2 * mm),
        Paragraph(
            "These are test scenarios, not test results. Nothing here proves the system fails; "
            "each case needs to be run against a real implementation or a test harness.",
            st["body"],
        ),
        Paragraph("The system", st["h2"]),
        Paragraph(_t(" ".join(run.description.split())), st["body"]),
    ]
    a = run.analysis
    if a.summary:
        story += [Spacer(1, 2 * mm), Paragraph(_t(a.summary), st["body"])]
    for label, items in [
        ("Components", a.components), ("Assumptions", a.assumptions),
        ("Constraints", a.constraints), ("Open questions", a.ambiguities),
    ]:
        if items:
            story.append(Paragraph(f"<b>{label}:</b> " + _t("; ".join(items)), st["body"]))
            story.append(Spacer(1, 1.5 * mm))

    story += [
        Paragraph("How priority is scored", st["h2"]),
        Paragraph(
            "Priority = severity x likelihood, each rated 1 to 5. "
            + _t(" ".join(f"{b}: " + r for b, r in zip(BANDS, ("20 to 25.", "12 to 19.", "6 to 11.", "1 to 5.")))),
            st["body"],
        ),
        Paragraph("Scenario index", st["h2"]),
    ]
    index = [[Paragraph(h, st["cellb"]) for h in ("ID", "Title", "Category", "S", "L", "P")]]
    for s in scenarios:
        index.append([
            Paragraph(_t(s.id), st["cell"]), Paragraph(_t(s.title), st["cell"]),
            Paragraph(_t(s.category.value), st["cell"]), str(s.severity), str(s.likelihood), str(s.priority),
        ])
    it = Table(index, colWidths=[16 * mm, 80 * mm, 44 * mm, 10 * mm, 10 * mm, 14 * mm], repeatRows=1)
    it.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HAZARD),
        ("BOX", (0, 0), (-1, -1), 1.6, INK),
        ("LINEBELOW", (0, 0), (-1, 0), 1.2, INK),
        ("LINEBELOW", (0, 1), (-1, -2), 0.4, CONCRETE),
        ("FONTNAME", (3, 1), (-1, -1), "Courier"), ("FONTSIZE", (3, 1), (-1, -1), 7.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story += [it, Paragraph("Scenarios", st["h2"])]
    story += [_scenario_block(s, st) for s in scenarios]

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return buf.getvalue()
