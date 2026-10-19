"""EdgeCase Foundry entry point. Wiring only; logic lives in foundry/."""
from __future__ import annotations

import streamlit as st

from foundry import storage
from foundry.llm import GroqClient, LLMError
from foundry.pipeline import run_pipeline
from foundry.ui import components, input_panel, results, sidebar, state, theme

st.set_page_config(page_title="EdgeCase Foundry", page_icon="⚠️", layout="wide", initial_sidebar_state="expanded")


def generate(request: input_panel.Request, engine: sidebar.EngineConfig) -> bool:
    """Run the pipeline with visible progress. Returns True if a new run was saved."""
    try:
        client = GroqClient(engine.api_key, engine.model)
        with st.status("Forging scenarios", expanded=True) as status:
            run = run_pipeline(client, request.description, request.count, request.focus, on_stage=st.write)
            status.update(label=f"Done: {len(run.scenarios)} scenarios", state="complete", expanded=False)
    except LLMError as exc:
        st.error(str(exc))
        return False
    run_id = storage.save_run(run)
    state.set_run(run.model_copy(update={"id": run_id}))
    return True


def main() -> None:
    theme.inject()
    storage.init_db()
    engine = sidebar.render()
    components.masthead()

    components.section(1, "Describe the system", "Input rules, constraints, and operational flows")
    left, right = st.columns([7, 5], gap="large")
    with left:
        request = input_panel.render()
    with right:
        components.rubric_panel()

    if request.submitted and generate(request, engine):
        st.rerun()  # refresh the sidebar history with the new run

    run = state.get_run()
    if run:
        results.render(run)
    else:
        components.empty_state()


main()
