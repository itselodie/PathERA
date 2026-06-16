# PathERA

**Emotion-Aware Reasoning Assistant** — Life Decision Simulator for the Productivity / Hackathon track.

Generic AI gives direct answers. PathERA guides students through dilemmas with context, emotions, hidden factors, decision trees, tradeoffs, scenario simulation, and personalized recommendations.

## Core pipeline (6 modules)

| # | Module | Role |
|---|--------|------|
| 1 | User input | Capture the dilemma in natural language |
| 2 | Context analyzer | Goals · constraints · emotions + **hidden factor detection** |
| 3 | Decision mapper | Build a branching decision tree |
| 4 | Tradeoff engine | Benefits & risks per option |
| 5 | Scenario simulator | "If you choose X → challenges → outcomes" |
| 6 | Recommendation | Based on **your** stated priorities |

## Quick start

```bash
cd PathERA
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env          # add OPENAI_API_KEY (optional)
streamlit run app.py
```

Open `http://localhost:8501`.

**Demo Mode** works without an API key — useful for hackathon demos and judging.

## Configuration

Create `.env` from `.env.example`:

```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

## Tech stack

- **Frontend:** Streamlit
- **Backend:** Python modular pipeline
- **AI:** OpenAI API (JSON structured outputs)
- **Viz:** Plotly + NetworkX (decision tree, tradeoff charts)

## Example prompts

- *"I want to study abroad but my family doesn't support it..."*
- *"I want to quit engineering. I'm exhausted and don't know if it's burnout or wrong fit."*
- *"Should I take a gap year or push through to finish my degree?"*

## Project structure

```
PathERA/
├── app.py                 # Streamlit UI (Module 1 + orchestration)
├── modules/
│   ├── context_analyzer.py
│   ├── decision_mapper.py
│   ├── tradeoff_engine.py
│   ├── scenario_simulator.py
│   ├── recommendation.py
│   └── llm_client.py
├── utils/
│   └── visualization.py
├── requirements.txt
└── .env.example
```

## Hackathon pitch angle

**Problem:** Students get generic AI advice on real life decisions.

**Solution:** PathERA reasons with emotion and context, surfaces hidden drivers (burnout, fear, wrong-fit), maps options visually, simulates futures, and recommends based on user priorities — not a one-size-fits-all answer.

**Killer feature:** Hidden factor detection — e.g. "I want to quit engineering" → burnout, exam stress, confidence gap, temporary frustration.

---

Built for hackathon demo. Not a substitute for professional counseling.
