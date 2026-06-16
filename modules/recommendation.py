"""Module 6 — Recommendation based on stated priorities."""

from __future__ import annotations

import json
from typing import Any

from modules.llm_client import call_llm_json

SYSTEM_PROMPT = """You are PathERA's Recommendation Engine.
Synthesize everything into a personalized recommendation — NOT a generic "do X" answer.

Return JSON:
{
  "recommended_option_id": "best-fit option id from decision tree",
  "recommended_label": "option name",
  "confidence": "low|medium|high",
  "rationale": "3-4 sentences tied to user's priorities, emotions, and hidden factors",
  "why_not_others": [
    {"option_id": "id", "reason": "why this is secondary for THIS user"}
  ],
  "immediate_next_steps": [
    {"step": "action", "timeframe": "this week|this month", "purpose": "why it matters"}
  ],
  "reflection_prompts": ["questions to sit with before committing"],
  "disclaimer": "brief note that this is guidance, not prescription"
}

Weight the user's stated priorities heavily. Acknowledge tradeoffs honestly."""


def generate_recommendation(
    user_input: str,
    context: dict[str, Any],
    decision_tree: dict[str, Any],
    tradeoffs: dict[str, Any],
    scenarios: dict[str, Any],
    priorities: dict[str, int],
) -> dict[str, Any]:
    payload = json.dumps(
        {
            "dilemma": user_input,
            "context": context,
            "decision_tree": decision_tree,
            "tradeoffs": tradeoffs,
            "scenarios": scenarios,
            "priorities": priorities,
        },
        indent=2,
    )
    return call_llm_json(SYSTEM_PROMPT, payload)


def demo_recommendation(
    user_input: str,
    context: dict[str, Any],
    decision_tree: dict[str, Any],
    tradeoffs: dict[str, Any],
    scenarios: dict[str, Any],
    priorities: dict[str, int],
) -> dict[str, Any]:
    options = decision_tree.get("options", [])
    if not options:
        return {"error": "No options in decision tree"}

    # Score options by alignment + priority weights
    top_priority = max(priorities, key=priorities.get) if priorities else "clarity"
    best = options[1] if len(options) > 1 else options[0]

    if top_priority == "family_harmony" and any("stay" in o["id"] for o in options):
        best = next(o for o in options if "stay" in o["id"])
    elif top_priority == "growth" and any("pivot" in o["id"] or "a" in o["id"] for o in options):
        best = next((o for o in options if "pivot" in o["id"] or o["id"] == "opt_a"), options[0])

    others = [o for o in options if o["id"] != best["id"]]

    return {
        "recommended_option_id": best["id"],
        "recommended_label": best["label"],
        "confidence": "medium",
        "rationale": (
            f"Given your top priority ({top_priority.replace('_', ' ')}), {best['label']} "
            "balances forward motion with room to address hidden factors like "
            f"{context.get('hidden_factors', [{}])[0].get('factor', 'underlying stress')}. "
            "It avoids an irreversible leap while still honoring your goals."
        ),
        "why_not_others": [
            {
                "option_id": o["id"],
                "reason": f"{o['label']} is viable but ranks lower against your stated priorities right now.",
            }
            for o in others[:2]
        ],
        "immediate_next_steps": [
            {
                "step": "Journal for 15 minutes on what 'success' looks like in 12 months",
                "timeframe": "this week",
                "purpose": "Separate fear from genuine misalignment",
            },
            {
                "step": f"Talk to one person who has done something like '{best['label']}'",
                "timeframe": "this month",
                "purpose": "Replace imagination with real data",
            },
            {
                "step": "Set a decision review date 4 weeks out",
                "timeframe": "this week",
                "purpose": "Prevent endless deliberation",
            },
        ],
        "reflection_prompts": [
            "What would you advise your best friend in this exact situation?",
            "Which option would you regret NOT trying?",
        ],
        "disclaimer": (
            "PathERA offers structured reasoning — the final choice is yours. "
            "Consider speaking with a counselor for deeply personal matters."
        ),
    }
