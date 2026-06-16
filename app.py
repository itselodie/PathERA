"""
PathERA — Emotion-Aware Reasoning Assistant
Life Decision Simulator | Hackathon Blueprint
"""

from __future__ import annotations

import streamlit as st

from modules import context_analyzer, decision_mapper, recommendation, scenario_simulator, tradeoff_engine
from modules.llm_client import get_client
from utils.visualization import build_decision_tree_figure, build_risk_benefit_bar, build_tradeoff_radar

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PathERA",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    .main-header h1 { color: #f8fafc; margin: 0; font-size: 2.4rem; font-weight: 700; }
    .main-header p { color: #a5b4fc; margin: 0.5rem 0 0; font-size: 1.1rem; }
    .module-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 0.5rem;
    }
    .hidden-factor {
        background: linear-gradient(90deg, rgba(251, 191, 36, 0.15), rgba(251, 191, 36, 0.05));
        border-left: 4px solid #fbbf24;
        padding: 1rem 1.25rem;
        border-radius: 0 12px 12px 0;
        margin: 0.75rem 0;
    }
    .rec-box {
        background: linear-gradient(135deg, rgba(34, 211, 238, 0.12), rgba(99, 102, 241, 0.12));
        border: 1px solid rgba(34, 211, 238, 0.4);
        padding: 1.5rem;
        border-radius: 16px;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a, #1e293b);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

PRIORITY_LABELS = {
    "growth": "Personal growth & learning",
    "financial": "Financial stability",
    "family_harmony": "Family harmony",
    "freedom": "Independence & freedom",
    "clarity": "Mental clarity & peace",
}

EXAMPLE_PROMPTS = [
    "I know what I want to do, but uncertainty, pressure, and competing priorities are making the decision difficult.",
    "I want to quit engineering. I'm exhausted and don't know if it's burnout or wrong fit.",
    "Should I take a gap year or push through to finish my degree this year?",
]


def run_pipeline(user_input: str, priorities: dict[str, int], demo_mode: bool) -> dict:
    """Execute all 6 modules sequentially."""
    if demo_mode:
        ctx = context_analyzer.demo_context(user_input)
        tree = decision_mapper.demo_decisions(user_input, ctx)
        trades = tradeoff_engine.demo_tradeoffs(user_input, ctx, tree)
        scenarios = scenario_simulator.demo_scenarios(user_input, ctx, tree, trades)
        rec = recommendation.demo_recommendation(user_input, ctx, tree, trades, scenarios, priorities)
    else:
        ctx = context_analyzer.analyze_context(user_input)
        tree = decision_mapper.map_decisions(user_input, ctx)
        trades = tradeoff_engine.analyze_tradeoffs(user_input, ctx, tree)
        scenarios = scenario_simulator.simulate_scenarios(user_input, ctx, tree, trades)
        rec = recommendation.generate_recommendation(
            user_input, ctx, tree, trades, scenarios, priorities
        )

    return {
        "context": ctx,
        "decision_tree": tree,
        "tradeoffs": trades,
        "scenarios": scenarios,
        "recommendation": rec,
    }


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧭 PathERA")
    st.caption("Emotion-Aware Reasoning Assistant")

    has_api = get_client() is not None
    demo_mode = st.toggle(
        "Demo Mode (no API key)",
        value=not has_api,
        help="Uses built-in sample reasoning. Turn off when OPENAI_API_KEY is set.",
    )

    if demo_mode:
        st.info("Demo Mode — add `OPENAI_API_KEY` to `.env` for live AI.")
    else:
        st.success("Live AI connected")

    st.divider()
    st.markdown("**Your priorities** (1 = low, 5 = high)")
    priorities = {}
    for key, label in PRIORITY_LABELS.items():
        priorities[key] = st.slider(label, 1, 5, 3, key=f"prio_{key}")

    st.divider()
    st.markdown("**Pipeline modules**")
    for i, name in enumerate(
        [
            "User input",
            "Context analyzer",
            "Decision mapper",
            "Tradeoff engine",
            "Scenario simulator",
            "Recommendation",
        ],
        1,
    ):
        st.markdown(f"`M{i}` {name}")

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="main-header">
        <h1>🧭 PathERA</h1>
        <p>Emotion-aware reasoning for life decisions — not generic answers, guided clarity.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Module 1: User input ───────────────────────────────────────────────────────
st.markdown(
    '<span class="module-badge">MODULE 1 — USER INPUT</span>',
    unsafe_allow_html=True
)

# Initialize session state
if "dilemma_input" not in st.session_state:
    st.session_state.dilemma_input = ""

# Callback for example buttons
def load_example(prompt):
    st.session_state.dilemma_input = prompt

col_in, col_ex = st.columns([3, 1])

with col_in:
    user_input = st.text_area(
        "Describe your dilemma",
        height=120,
        placeholder='e.g. "I know what I want to do, but uncertainty, fear, and pressure are making the decision difficult..."',
        key="dilemma_input",
    )

with col_ex:
    st.markdown("### Try an example")

    for idx, prompt in enumerate(EXAMPLE_PROMPTS):
        st.button(
            prompt,
            key=f"example_{idx}",
            use_container_width=True,
            on_click=load_example,
            args=(prompt,)
        )

analyze = st.button(
    "🔍 Analyze my path",
    type="primary"
)

if analyze:
    if not st.session_state.dilemma_input or len(st.session_state.dilemma_input.strip()) < 10:
        st.warning("Please describe your dilemma in at least a few sentences.")
    elif not context_analyzer.is_valid_dilemma(st.session_state.dilemma_input.strip()):
        st.warning(
            "\u26a0\ufe0f PathERA couldn\'t detect a meaningful decision dilemma.\n\n"
            "Try describing a difficult choice, career decision, or life transition you\'re facing.\n\n"
            "**Example:** *\"I want to study abroad but my family disagrees.\"*"
        )
    else:
        with st.spinner("Running PathERA pipeline (6 modules)…"):
            try:
                st.session_state["results"] = run_pipeline(
                    st.session_state.dilemma_input.strip(),
                    priorities,
                    demo_mode,
                )
            except Exception as e:
                st.error(f"Pipeline error: {e}")

# ── Results ──────────────────────────────────────────────────────────────────
if "results" in st.session_state:
    r = st.session_state["results"]
    ctx = r["context"]
    tree = r["decision_tree"]
    trades = r["tradeoffs"]
    scenarios = r["scenarios"]
    rec = r["recommendation"]

    st.divider()

    # Module 2: Context
    st.markdown('<span class="module-badge">MODULE 2 — CONTEXT ANALYZER</span>', unsafe_allow_html=True)
    st.markdown(f"**Summary:** {ctx.get('summary', '')}")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Goals**")
        for g in ctx.get("goals", []):
            st.markdown(f"- {g}")
    with c2:
        st.markdown("**Constraints**")
        for c in ctx.get("constraints", []):
            st.markdown(f"- {c}")
    with c3:
        st.markdown("**Emotions**")
        for e in ctx.get("emotions", []):
            st.markdown(f"- **{e.get('name', '?')}** ({e.get('intensity', '?')})")

    st.markdown("#### 🔍 Hidden factor detection")
    for hf in ctx.get("hidden_factors", []):
        st.markdown(
            f"""<div class="hidden-factor">
            <strong>{hf.get('factor', '')}</strong> · likelihood: {hf.get('likelihood', '?')}<br>
            <em>{hf.get('reasoning', '')}</em>
            </div>""",
            unsafe_allow_html=True,
        )
        for q in hf.get("questions_to_explore", []):
            st.caption(f"💭 {q}")

    st.divider()

    # Module 3: Decision tree
    st.markdown('<span class="module-badge">MODULE 3 — DECISION MAPPER</span>', unsafe_allow_html=True)
    st.markdown(f"**{tree.get('root_question', '')}**")
    st.plotly_chart(build_decision_tree_figure(tree), use_container_width=True)

    for opt in tree.get("options", []):
        with st.expander(f"**{opt['label']}** — {opt.get('description', '')}", expanded=True):
            if opt.get("prerequisites"):
                st.markdown("**Prerequisites:** " + ", ".join(opt["prerequisites"]))
            for sub in opt.get("sub_options", []):
                st.markdown(f"- ↳ {sub['label']}: {sub.get('description', '')}")

    st.divider()

    # Module 4: Tradeoffs
    st.markdown('<span class="module-badge">MODULE 4 — TRADEOFF ENGINE</span>', unsafe_allow_html=True)
    tc1, tc2 = st.columns(2)
    with tc1:
        st.plotly_chart(build_tradeoff_radar(trades), use_container_width=True)
    with tc2:
        st.plotly_chart(build_risk_benefit_bar(trades), use_container_width=True)

    for t in trades.get("tradeoffs", []):
        with st.expander(f"{t['option_label']} — alignment {t.get('alignment_score', '?')}/100", expanded=True):
            bcol, rcol = st.columns(2)
            with bcol:
                st.markdown("**Benefits**")
                for b in t.get("benefits", []):
                    st.markdown(f"- ✅ {b['point']} (*{b.get('impact', '')}*)")
            with rcol:
                st.markdown("**Risks**")
                for risk in t.get("risks", []):
                    st.markdown(f"- ⚠️ {risk['point']} — _{risk.get('mitigation', '')}_")

            pa = t.get("priority_alignment")
            if pa:
                st.markdown("**Priority alignment scores**")
                pa_labels = {
                    "growth": "Personal growth",
                    "financial": "Financial stability",
                    "family_harmony": "Family harmony",
                    "freedom": "Independence",
                    "clarity": "Mental clarity",
                }
                for key, label in pa_labels.items():
                    score = pa.get(key, 50)
                    st.progress(score / 100, text=f"{label}: {score}/100")

    if trades.get("key_tensions"):
        st.markdown("**Key tensions:** " + " · ".join(trades["key_tensions"]))

    st.divider()

    # Module 5: Scenarios
    st.markdown('<span class="module-badge">MODULE 5 — SCENARIO SIMULATOR ⭐</span>', unsafe_allow_html=True)
    for sc in scenarios.get("scenarios", []):
        with st.expander(f"📖 {sc['option_label']} — {sc.get('timeline', '')} outlook", expanded=True):
            st.markdown(sc.get("narrative", ""))
            st.markdown("**Challenges**")
            for ch in sc.get("challenges", []):
                st.markdown(
                    f"- {ch['challenge']} (p: {ch.get('probability', '?')}) → *{ch.get('coping', '')}*"
                )
            st.markdown("**Positive outcomes:** " + ", ".join(sc.get("positive_outcomes", [])))
            st.markdown("**Negative outcomes:** " + ", ".join(sc.get("negative_outcomes", [])))

    wc = scenarios.get("wildcard", {})
    if wc:
        st.info(f"💡 **Insight:** {wc.get('insight', '')}  \n**Blind spot:** {wc.get('blind_spot', '')}")

    st.divider()

    # Module 6: Recommendation
    st.markdown('<span class="module-badge">MODULE 6 — RECOMMENDATION</span>', unsafe_allow_html=True)
    st.markdown(
        f"""<div class="rec-box">
        <h3 style="margin-top:0;color:#22d3ee;">Recommended: {rec.get('recommended_label', '')}</h3>
        <p style="color:#e2e8f0;">{rec.get('rationale', '')}</p>
        <p style="font-size:0.85rem;color:#94a3b8;">Confidence: {rec.get('confidence', '?')}</p>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown("**Why not the other paths?**")
    for w in rec.get("why_not_others", []):
        st.markdown(f"- {w.get('reason', '')}")

    st.markdown("**Immediate next steps**")
    for step in rec.get("immediate_next_steps", []):
        st.markdown(f"1. **{step.get('step', '')}** ({step.get('timeframe', '')}) — {step.get('purpose', '')}")

    st.markdown("**Sit with these questions**")
    for rp in rec.get("reflection_prompts", []):
        st.markdown(f"- _{rp}_")

    st.caption(rec.get("disclaimer", ""))
