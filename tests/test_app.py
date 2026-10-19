"""Headless render of the real app with Streamlit's AppTest. Catches wiring and runtime errors."""
from streamlit.testing.v1 import AppTest

from foundry import scoring
from foundry.schemas import Run, Stats, SystemAnalysis
from tests.test_core import mk


def _run():
    sc = scoring.rank_and_label([scoring.score(mk()), scoring.score(mk(title="Clock skew", cat="State and timing", desc="Clocks differ by $40 and 40 seconds", sev=4, lik=4))])
    return Run(id=None, created_at="2026-10-19T10:00:00+00:00", description="Attendance system", model="fake",
               analysis=SystemAnalysis(summary="Summary", components=["Reader"], ambiguities=["What about <script>?"]),
               scenarios=sc, stats=Stats(requested=2, generated=2, rejected=0, duplicates_removed=0))


def test_empty_state_renders_and_generate_is_disabled(tmp_path, monkeypatch):
    monkeypatch.setenv("EDGECASE_DB", str(tmp_path / "a.db"))
    at = AppTest.from_file("app.py", default_timeout=30).run()
    assert not at.exception
    gen = [b for b in at.button if b.label == "Generate edge cases"][0]
    assert gen.disabled


def test_sample_enables_generate_and_missing_key_errors_cleanly(tmp_path, monkeypatch):
    monkeypatch.setenv("EDGECASE_DB", str(tmp_path / "b.db"))
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    at = AppTest.from_file("app.py", default_timeout=30).run()
    [b for b in at.button if b.label == "University attendance"][0].click().run()
    assert not at.exception and len(at.text_area[0].value) > 100
    [b for b in at.button if b.label == "Generate edge cases"][0].click().run()
    assert not at.exception
    assert any("API key" in e.value for e in at.error)


def test_results_view_renders(tmp_path, monkeypatch):
    monkeypatch.setenv("EDGECASE_DB", str(tmp_path / "c.db"))
    at = AppTest.from_file("app.py", default_timeout=30)
    at.session_state["run"] = _run()
    at.run()
    assert not at.exception
    html = " ".join(m.value for m in at.markdown)
    assert "EC-01" in html and "&#36;40" in html and "<script>" not in html and "&lt;script&gt;" in html
