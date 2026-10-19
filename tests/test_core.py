import pytest

from foundry import scoring, storage
from foundry.dedupe import dedupe
from foundry.exporters import to_csv_bytes, to_pdf_bytes
from foundry.filtering import apply_filters
from foundry.generator import generate
from foundry.pipeline import run_pipeline
from foundry.schemas import Category, Scenario, SystemAnalysis


def mk(title="Duplicate scan", cat="Duplicate request", sev=3, lik=5, desc="Student scans twice within five seconds", **kw):
    base = dict(
        title=title, category=cat, description=desc, risk="Attendance counted twice", severity=sev, likelihood=lik,
        input_conditions="Valid card and open session", steps=["Scan the card", "Scan again after 2 seconds"],
        expected_result="One record exists", pass_criteria="Exactly one row", fail_criteria="Two rows", suggested_fix="Idempotency key",
    )
    base.update(kw)
    return Scenario(**base)


class FakeClient:
    model = "fake-model"

    def __init__(self, scenarios):
        self.scenarios = scenarios

    def generate_json(self, system, prompt, temperature=0.7, attempts=3):
        if "Return JSON in exactly this shape (3 to 7" in prompt:
            return {"summary": "An attendance system.", "components": ["Card reader", "API"], "assumptions": ["Wi-Fi is reliable"]}
        return {"scenarios": self.scenarios}


RAW = lambda **kw: {  # noqa: E731
    "title": "Expired card", "category": "invalid input", "description": "A card expired yesterday is scanned",
    "risk": "Unauthorised attendance", "severity": 6, "likelihood": "2", "input_conditions": "Expired card",
    "steps": "1. Scan\n2. Observe the reader", "expected_result": "Rejected", "pass_criteria": "Error shown",
    "fail_criteria": "Attendance marked", "suggested_fix": "Check expiry server-side", **kw,
}


def test_priority_and_bands():
    assert scoring.priority(5, 5) == 25
    assert [scoring.band(x) for x in (25, 20, 19, 12, 11, 6, 5, 1)] == ["Critical", "Critical", "High", "High", "Medium", "Medium", "Low", "Low"]


def test_schema_coerces_and_clamps():
    s = Scenario(**RAW())
    assert s.severity == 5 and s.likelihood == 2 and s.category is Category.INVALID_INPUT
    assert s.steps == ["Scan", "Observe the reader"]


def test_schema_rejects_unknown_category_and_short_steps():
    with pytest.raises(ValueError):
        Scenario(**RAW(category="vibes"))
    with pytest.raises(ValueError):
        Scenario(**RAW(steps=["only one"]))


def test_category_and_spelling_variants():
    assert Category.coerce("State & timing") is Category.STATE
    assert Category.coerce("environment and scale") is Category.ENVIRONMENT


def test_dedupe_keeps_higher_priority():
    a = scoring.score(mk(sev=5, lik=4))
    b = scoring.score(mk(title="Duplicate scan twice", sev=2, lik=2, desc="A student scans twice within five seconds"))
    c = scoring.score(mk(title="Clock skew at deadline", cat="State and timing", desc="Server and reader clocks differ by 40 seconds"))
    kept, removed = dedupe([b, a, c])
    assert removed == 1 and a in kept and b not in kept and c in kept


def test_generator_counts_rejections():
    bad = RAW(category="nonsense")
    valid, rejected = generate(FakeClient([RAW(), bad]), "desc", SystemAnalysis(), 2)
    assert len(valid) == 1 and rejected == 1


def test_pipeline_end_to_end(tmp_path):
    items = [RAW(), RAW(title="Clock skew", category="State and timing", description="Clocks differ by 40 seconds at the deadline", severity=3, likelihood=3)]
    run = run_pipeline(FakeClient(items), "A university attendance system with ID cards", 10)
    assert [s.id for s in run.scenarios] == ["EC-01", "EC-02"]
    assert run.scenarios[0].priority >= run.scenarios[1].priority
    db = tmp_path / "t.db"
    storage.init_db(db)
    rid = storage.save_run(run, db)
    loaded = storage.load_run(rid, db)
    assert loaded and loaded.id == rid and len(loaded.scenarios) == 2
    assert storage.list_runs(path=db)[0].scenario_count == 2
    storage.delete_run(rid, db)
    assert storage.load_run(rid, db) is None


def test_filters():
    sc = [scoring.score(mk()), scoring.score(mk(title="Expired card", cat="Invalid input", sev=1, lik=1, desc="Expired card scanned at the door"))]
    assert len(apply_filters(sc, [Category.INVALID_INPUT])) == 1
    assert len(apply_filters(sc, min_priority=10)) == 1
    assert len(apply_filters(sc, query="EXPIRED")) == 1
    assert len(apply_filters(sc, bands=["Low"])) == 1


def test_csv_neutralises_formulas_and_pdf_builds():
    s = scoring.rank_and_label([scoring.score(mk(suggested_fix="=HYPERLINK(\"http://x\")", title="Curly \u201cquote\u201d \u2192 arrow"))])
    csv = to_csv_bytes(s).decode("utf-8-sig")
    assert "'=HYPERLINK" in csv
    from foundry.schemas import Run, Stats
    run = Run(created_at="2026-10-19T00:00:00", description="A <b>system</b> costing $5", model="m", analysis=SystemAnalysis(summary="s"), scenarios=s,
              stats=Stats(requested=1, generated=1, rejected=0, duplicates_removed=0))
    assert to_pdf_bytes(run, s).startswith(b"%PDF")
