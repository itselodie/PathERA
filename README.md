# 🧭 PathERA

### Emotion-Aware Reasoning Assistant

**PathERA** is an AI-powered decision intelligence system designed to help students and young adults navigate difficult life decisions with greater clarity, confidence, and self-awareness.

Most AI assistants provide generic advice. PathERA takes a different approach.

Instead of immediately telling users what to do, it guides them through a structured reasoning process that uncovers hidden emotional drivers, evaluates tradeoffs, simulates future outcomes, and generates recommendations aligned with their personal priorities.

---

## 🚀 The Problem

Students frequently face complex life decisions:

* Should I study abroad?
* Should I quit engineering?
* Should I take a gap year?
* Should I choose passion or financial stability?
* Should I move away from family for opportunities?

Traditional AI tools often provide surface-level answers without understanding the deeper emotional and contextual factors behind these dilemmas.

---

## 💡 The Solution

PathERA acts as an **Emotion-Aware Reasoning Assistant**.

It combines structured decision-making with emotional context to help users understand:

* What options they have
* What tradeoffs each option creates
* What hidden factors may be influencing them
* What future outcomes are most likely
* Which path best aligns with their priorities

---

# 🧠 Core Pipeline

| Module                         | Purpose                                                                |
| ------------------------------ | ---------------------------------------------------------------------- |
| **M1 — User Input**            | Capture the dilemma in natural language                                |
| **M2 — Context Analyzer**      | Extract goals, constraints, emotions, stakeholders, and hidden factors |
| **M3 — Decision Mapper**       | Generate realistic decision pathways                                   |
| **M4 — Tradeoff Engine**       | Compare benefits, risks, and priority alignment                        |
| **M5 — Scenario Simulator**    | Forecast possible future outcomes                                      |
| **M6 — Recommendation Engine** | Generate actionable recommendations                                    |

---

# ⭐ Killer Feature: Hidden Factor Detection

PathERA doesn't only analyze what users say.

It attempts to identify what they may not be saying.

Example:

### User Input

> "I want to quit engineering."

### Possible Hidden Factors

* Academic burnout
* Fear of failure
* Confidence gap after setbacks
* Social comparison
* Wrong-fit vs. wrong-timing confusion

This allows recommendations to address root causes rather than symptoms.

---

# 🎯 Example Dilemmas

* "I want to study abroad but my family doesn't support it."
* "I have two job offers. One pays more, one feels meaningful."
* "I think I want to leave engineering but I'm not sure if it's burnout."
* "Should I take a gap year or finish my degree first?"

---

# 🛠 Tech Stack

### Frontend

* Streamlit

### Backend

* Python
* Modular reasoning pipeline

### AI

* OpenAI API
* Structured JSON outputs

### Visualization

* Plotly
* NetworkX

---

# ⚙️ Quick Start

```bash
git clone https://github.com/itselodie/PathERA.git

cd PathERA

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

copy .env.example .env

streamlit run app.py
```

Open:

http://localhost:8501

---

# 🔑 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o-mini
```

PathERA also supports **Demo Mode**, allowing the application to run without an API key for hackathon demonstrations.

---

# 🌐 Live Demo

Streamlit Deployment:

https://pathera-kdupfsqopuubmttvqfhmu2.streamlit.app/

---

# 📂 Project Structure

```text
PathERA/
├── app.py
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

---

# 🏆 Hackathon Pitch

### Problem

People receive generic AI advice for deeply personal decisions.

### Solution

PathERA introduces emotion-aware reasoning, hidden-factor detection, tradeoff evaluation, future scenario simulation, and personalized recommendations.

### Impact

Helping students and young adults make important life decisions with greater clarity, confidence, and self-awareness.

---

## ⚠️ Disclaimer

PathERA is designed for reflection, guidance, and structured reasoning.

It is **not a substitute for professional counseling, therapy, legal advice, financial advice, or medical advice.**
