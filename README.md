# EdgeCase Foundry

Describe a system in plain English. Get 10 to 20 edge-case scenarios, each with risk impact, test execution steps,
expected result, pass/fail criteria, and a suggested fix. Scored with a deterministic rubric, plotted with interactive Plotly charts, saved to SQLite, and exportable as CSV or PDF. Built with a clean, minimalist UI using the Poppins font.

**It generates scenarios. It does not prove a system is broken.** Pass/fail verification needs a runnable implementation or a separate test harness.

## Quickstart

### 1. Setup Environment
```bash
python -m venv .venv

# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure API Key
Copy `.env.example` to `.env` and add your free Groq API key:
```bash
cp .env.example .env
```
In `.env`:
```env
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=openai/gpt-oss-120b
```
*(Get a free key from [Groq Console](https://console.groq.com/keys))*.

### 3. Run the App

**PowerShell (Windows):**
```powershell
.\run.ps1
```

**Command Prompt / Batch:**
```cmd
run.bat
```

**Standard Streamlit CLI:**
```bash
streamlit run app.py
```

## How It Works

| Step | Module | What Happens |
|---|---|---|
| 1 Describe | `ui/input_panel.py` | Plain English description, scenario count, optional category focus |
| 2 Analyze | `analyzer.py` | Groq lists components, actors, assumptions, constraints, and open questions |
| 3 Generate | `generator.py` | Groq outputs scenarios in JSON; each item is individually validated |
| 4 Validate & Score | `schemas.py`, `scoring.py`, `dedupe.py` | Pydantic schema validation, priority = severity × likelihood, near-duplicates dropped |
| 5 Review & Export | `ui/results.py`, `exporters.py` | Interactive filters, risk distribution matrix, CSV and PDF exports |

## Layout

```
app.py                  Wiring entry point
foundry/
  config.py             Runtime configuration & dynamic .env loading
  llm.py                Groq client with native JSON-object mode & retry backoff
  analyzer.py           System decomposition & boundary analysis
  generator.py          Scenario synthesis with structured prompting
  pipeline.py           End-to-end execution pipeline
  schemas.py            Pydantic models for runs, scenarios, analysis
  scoring.py            Deterministic rubric scoring & risk bands
  dedupe.py             Fuzzy deduplication
  filtering.py          Multi-attribute filtering & search
  storage.py            SQLite run persistence
  exporters.py          CSV and PDF document generation
  ui/
    theme.py            Minimalist theme system (Poppins font only)
    components.py       Stateless HTML renderers & badges
    charts.py           Plotly risk distribution matrix & category charts
    sidebar.py          Saved runs history & engine status
    input_panel.py      Description input & 2x2 sample grid
    results.py          Results view, analytics, filter controls
    state.py            Streamlit session state management
tests/                  Pytest suite covering core logic and headless app renders
```

## Tests

```bash
python -m pytest -q
```

## Notes

- Uses Groq for ultra-fast structured JSON generation.
- CSV cells starting with `=`, `+`, `-`, or `@` are automatically sanitized to block spreadsheet formula injection.
- Run history is automatically preserved locally in SQLite (`data/foundry.db`).
