"""Module 2 — Context analyzer: goals, constraints, emotions, hidden factors."""

from __future__ import annotations

from typing import Any

from modules.llm_client import call_llm_json

SYSTEM_PROMPT = """You are PathERA's Context Analyzer for life decisions.
Extract structured context from the user's dilemma. Be empathetic and insightful.

Return JSON with this exact schema:
{
  "summary": "one-sentence restatement of the dilemma",
  "goals": ["explicit goals the user wants"],
  "constraints": ["limitations, obligations, or blockers"],
  "emotions": [{"name": "emotion", "intensity": "low|medium|high", "evidence": "quote or paraphrase"}],
  "hidden_factors": [
    {
      "factor": "possible unstated driver (e.g. burnout, fear, peer pressure)",
      "likelihood": "low|medium|high",
      "reasoning": "why this might be underlying the stated problem",
      "questions_to_explore": ["reflective question for the user"]
    }
  ],
  "stakeholders": ["people affected by this decision"],
  "time_horizon": "immediate|short-term|long-term"
}

Detect 3-5 hidden factors the user may not have named. This is PathERA's killer feature.
Focus on students and young adults making career, education, and life path decisions."""


def analyze_context(user_input: str) -> dict[str, Any]:
    return call_llm_json(SYSTEM_PROMPT, user_input)


def demo_context(user_input: str) -> dict[str, Any]:
    """Offline demo when no API key is available."""
    lower = user_input.lower()
    hidden = []

    if any(w in lower for w in ("quit", "drop", "leave", "engineering", "course")):
        hidden = [
            {
                "factor": "Academic burnout",
                "likelihood": "high",
                "reasoning": "Wanting to quit often peaks during exam seasons or after sustained overload.",
                "questions_to_explore": [
                    "When did you last feel genuinely curious about your field?",
                    "Is the stress temporary (one semester) or chronic?",
                ],
            },
            {
                "factor": "Wrong-fit vs. wrong-timing",
                "likelihood": "medium",
                "reasoning": "Frustration with one subject doesn't always mean the entire path is wrong.",
                "questions_to_explore": [
                    "Which parts of engineering do you still enjoy, if any?",
                    "Would a pivot within tech (design, product, data) feel better than leaving entirely?",
                ],
            },
            {
                "factor": "Confidence gap after setbacks",
                "likelihood": "medium",
                "reasoning": "Failed exams or comparisons with peers can make quitting feel like the only dignified exit.",
                "questions_to_explore": [
                    "Are you measuring yourself against an unrealistic benchmark?",
                ],
            },
        ]
        goals = ["Find a career path that feels sustainable", "Reduce daily dread about studies"]
        constraints = ["Sunk cost of current degree", "Family expectations", "Financial investment"]
        emotions = [
            {"name": "frustration", "intensity": "high", "evidence": "desire to quit"},
            {"name": "doubt", "intensity": "medium", "evidence": "questioning fit"},
        ]
    elif any(w in lower for w in ("abroad", "foreign", "overseas", "study")):
        hidden = [
            {
                "factor": "Fear of disappointing family",
                "likelihood": "high",
                "reasoning": "Family tension often masks love and risk-aversion, not opposition to your growth.",
                "questions_to_explore": [
                    "What specific worry does your family voice — safety, cost, or losing closeness?",
                ],
            },
            {
                "factor": "Imposter syndrome about readiness",
                "likelihood": "medium",
                "reasoning": "Students sometimes delay big moves because they feel 'not ready' despite being qualified.",
                "questions_to_explore": [
                    "Would you advise a friend with your profile to apply?",
                ],
            },
            {
                "factor": "Romanticized escape from current environment",
                "likelihood": "medium",
                "reasoning": "Study abroad can be framed as a fresh start when local stress is the real pain point.",
                "questions_to_explore": [
                    "What problems would still follow you abroad?",
                ],
            },
        ]
        goals = ["Gain international exposure", "Advance education or career"]
        constraints = ["Family approval", "Tuition and living costs", "Visa and admission uncertainty"]
        emotions = [
            {"name": "ambition", "intensity": "high", "evidence": "wants to study abroad"},
            {"name": "guilt", "intensity": "medium", "evidence": "family concerns mentioned"},
        ]
    else:
        hidden = [
            {
                "factor": "Decision fatigue",
                "likelihood": "medium",
                "reasoning": "Major life choices are cognitively heavy; paralysis can feel like having no good options.",
                "questions_to_explore": ["What would 'good enough' look like for the next 12 months?"],
            },
            {
                "factor": "Social comparison",
                "likelihood": "medium",
                "reasoning": "Peers' paths can distort what feels right for you.",
                "questions_to_explore": ["Whose opinion matters most — and why?"],
            },
        ]
        goals = ["Clarity on next step", "Alignment between values and action"]
        constraints = ["Limited information", "Multiple competing priorities"]
        emotions = [{"name": "uncertainty", "intensity": "high", "evidence": "seeking guidance"}]

    return {
        "summary": f"You're navigating a meaningful life decision: {user_input[:120]}...",
        "goals": goals,
        "constraints": constraints,
        "emotions": emotions,
        "hidden_factors": hidden,
        "stakeholders": ["You", "Family", "Future self"],
        "time_horizon": "long-term",
    }


def is_valid_dilemma(user_input: str) -> bool:
    """Check if input contains a real life dilemma worth analyzing."""
    lower = user_input.lower().strip()

    if len(lower.split()) < 5:
        return False

    dilemma_signals = [
        "should i", "should we", "i want to", "i need to", "i have to",
        "i'm thinking", "thinking about", "considering",
        "don't know", "not sure", "unsure", "confused",
        "struggling", "difficult", "torn between",
        "can't decide", "help me decide",
        "quit", "leave", "stay", "switch", "change", "move",
        "study", "career", "job", "degree", "major", "college",
        "family", "parents", "relationship", "abroad", "gap year",
        "burnout", "exhausted", "stressed", "overwhelmed",
        "opportunity", "offer", "internship", "choice", "decision",
        "but", "however", "although", "conflict", "dilemma",
        "worried", "scared", "afraid", "anxious",
        "what if", "whether", "or not",
    ]

    return any(signal in lower for signal in dilemma_signals)


def is_valid_dilemma(user_input: str) -> bool:
    lower = user_input.lower().strip()
    if len(lower.split()) < 5:
        return False
    dilemma_signals = [
        'should i', 'should we', 'i want to', 'i need to', 'i have to',
        'thinking about', 'considering', "don't know", 'not sure', 'unsure',
        'confused', 'struggling', 'difficult', 'torn between', 'quit', 'leave',
        'stay', 'switch', 'change', 'move', 'study', 'career', 'job', 'degree',
        'major', 'college', 'family', 'parents', 'abroad', 'gap year', 'burnout',
        'exhausted', 'stressed', 'overwhelmed', 'opportunity', 'offer',
        'internship', 'choice', 'decision', 'but', 'however', 'although',
        'conflict', 'dilemma', 'worried', 'scared', 'afraid', 'anxious',
        'what if', 'whether', 'or not',
    ]
    return any(signal in lower for signal in dilemma_signals)


def is_valid_dilemma(user_input: str) -> bool:
    lower = user_input.lower().strip()
    if len(lower.split()) < 5:
        return False
    dilemma_signals = [
        'should i', 'should we', 'i want to', 'i need to', 'i have to',
        'thinking about', 'considering', "don't know", 'not sure', 'unsure',
        'confused', 'struggling', 'difficult', 'torn between', 'quit', 'leave',
        'stay', 'switch', 'change', 'move', 'study', 'career', 'job', 'degree',
        'major', 'college', 'family', 'parents', 'abroad', 'gap year', 'burnout',
        'exhausted', 'stressed', 'overwhelmed', 'opportunity', 'offer',
        'internship', 'choice', 'decision', 'but', 'however', 'although',
        'conflict', 'dilemma', 'worried', 'scared', 'afraid', 'anxious',
        'what if', 'whether', 'or not',
    ]
    return any(signal in lower for signal in dilemma_signals)
