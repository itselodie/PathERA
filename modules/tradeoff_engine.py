"""Module 4 — Tradeoff engine: benefits and risks per option."""

from __future__ import annotations

import json
from typing import Any

from modules.llm_client import call_llm_json

SYSTEM_PROMPT = """You are PathERA's Tradeoff Engine.
Analyze benefits and risks for each decision option, grounded in the user's context.

Return JSON:
{
  "tradeoffs": [
    {
      "option_id": "matches decision tree id",
      "option_label": "name",
      "benefits": [{"point": "benefit", "impact": "low|medium|high", "reasoning": "why"}],
      "risks": [{"point": "risk", "severity": "low|medium|high", "mitigation": "how to reduce"}],
      "effort": "low|medium|high",
      "reversibility": "low|medium|high",
      "alignment_score": 0-100,
      "priority_alignment": {"growth": 0-100, "financial": 0-100, "family_harmony": 0-100, "freedom": 0-100, "clarity": 0-100}
    }
  ],
  "key_tensions": ["core tradeoffs between options in plain language"]
}

Be specific to THIS user's emotions, constraints, and hidden factors — not generic advice."""


def analyze_tradeoffs(
    user_input: str,
    context: dict[str, Any],
    decision_tree: dict[str, Any],
) -> dict[str, Any]:
    payload = json.dumps(
        {"dilemma": user_input, "context": context, "decision_tree": decision_tree},
        indent=2,
    )
    return call_llm_json(SYSTEM_PROMPT, payload)

def _detect_topic(user_input: str) -> str:
    lower = user_input.lower()
    if any(w in lower for w in ("abroad", "foreign", "overseas", "international")):
        return "abroad"
    if any(w in lower for w in ("quit", "engineering", "drop", "change major")):
        return "engineering"
    if any(w in lower for w in ("gap year", "pause", "take a break")):
        return "gap_year"
    if any(w in lower for w in ("internship", "job", "work", "career", "move", "relocat", "another city", "new city", "different city")):
        return "career"
    return "general"


def demo_tradeoffs(
    user_input: str,
    context: dict[str, Any],
    decision_tree: dict[str, Any],
) -> dict[str, Any]:
    topic = _detect_topic(user_input)
    options = decision_tree.get("options", [])

    # Topic-specific tradeoff data
    TRADEOFF_DATA = {
        "abroad": [
            {
                "benefits": [
                    {"point": "International exposure & network", "impact": "high", "reasoning": "Opens global career doors unavailable locally."},
                    {"point": "Personal independence & confidence", "impact": "high", "reasoning": "Living abroad builds resilience fast."},
                ],
                "risks": [
                    {"point": "High financial cost", "severity": "high", "mitigation": "Research scholarships, part-time work visas."},
                    {"point": "Family distance & guilt", "severity": "medium", "mitigation": "Set regular video call schedule before leaving."},
                ],
                "alignment_score": 84,
                "priority_alignment": {"growth": 92, "financial": 45, "family_harmony": 40, "freedom": 95, "clarity": 70},
            },
            {
                "benefits": [
                    {"point": "Gather more info before committing", "impact": "medium", "reasoning": "Reduces regret risk on a big decision."},
                    {"point": "Time to strengthen application", "impact": "medium", "reasoning": "Better prep = better program options."},
                ],
                "risks": [
                    {"point": "Opportunity cost of delay", "severity": "medium", "mitigation": "Set a hard deadline — no more than 6 months."},
                    {"point": "Indecision can become habit", "severity": "medium", "mitigation": "Define exactly what info would change your mind."},
                ],
                "alignment_score": 68,
                "priority_alignment": {"growth": 60, "financial": 70, "family_harmony": 75, "freedom": 55, "clarity": 80},
            },
            {
                "benefits": [
                    {"point": "Lower cost, family support nearby", "impact": "high", "reasoning": "Reduces financial and emotional strain."},
                    {"point": "Build credentials first", "impact": "medium", "reasoning": "Local experience can strengthen future abroad applications."},
                ],
                "risks": [
                    {"point": "Potential long-term regret", "severity": "high", "mitigation": "Revisit this decision in 1 year with fresh perspective."},
                    {"point": "Fewer international connections", "severity": "medium", "mitigation": "Join global online communities and conferences."},
                ],
                "alignment_score": 55,
                "priority_alignment": {"growth": 50, "financial": 90, "family_harmony": 88, "freedom": 30, "clarity": 60},
            },
        ],
        "engineering": [
            {
                "benefits": [
                    {"point": "Reduces immediate burnout pressure", "impact": "high", "reasoning": "Changing specialization removes the specific pain point."},
                    {"point": "Preserves degree investment", "impact": "high", "reasoning": "Credits transfer, time isn't fully lost."},
                ],
                "risks": [
                    {"point": "New area may have same issues", "severity": "medium", "mitigation": "Shadow someone in target field before committing."},
                    {"point": "Transition delay adds semester", "severity": "low", "mitigation": "Plan credit transfer early with advisor."},
                ],
                "alignment_score": 80,
                "priority_alignment": {"growth": 78, "financial": 72, "family_harmony": 80, "freedom": 65, "clarity": 85},
            },
            {
                "benefits": [
                    {"point": "Engineering skills transfer to tech-adjacent roles", "impact": "high", "reasoning": "PM, UX, data roles value technical background."},
                    {"point": "Avoids full restart cost", "impact": "medium", "reasoning": "Partial degree + portfolio is viable in many fields."},
                ],
                "risks": [
                    {"point": "Identity confusion during transition", "severity": "high", "mitigation": "Talk to people who've made similar pivots."},
                    {"point": "Skills gap in new field", "severity": "medium", "mitigation": "Take 1-2 targeted online courses while finishing."},
                ],
                "alignment_score": 70,
                "priority_alignment": {"growth": 85, "financial": 60, "family_harmony": 55, "freedom": 82, "clarity": 65},
            },
            {
                "benefits": [
                    {"point": "Clean break removes ambiguity", "impact": "medium", "reasoning": "Some people need a full reset to move forward."},
                    {"point": "Pursue genuine interest directly", "impact": "high", "reasoning": "Alignment with real passion improves long-term outcomes."},
                ],
                "risks": [
                    {"point": "Sunk cost of current degree lost", "severity": "high", "mitigation": "Audit transferable credits before deciding."},
                    {"point": "Family and financial pressure", "severity": "high", "mitigation": "Build 3-month financial runway before transition."},
                ],
                "alignment_score": 58,
                "priority_alignment": {"growth": 72, "financial": 30, "family_harmony": 25, "freedom": 90, "clarity": 70},
            },
        ],
        "gap_year": [
            {
                "benefits": [
                    {"point": "Real-world clarity before committing", "impact": "high", "reasoning": "Gap year experiences often crystallize career direction."},
                    {"point": "Prevents burnout from pushing through", "impact": "high", "reasoning": "Mental reset improves performance when you return."},
                ],
                "risks": [
                    {"point": "Resume gap perception", "severity": "medium", "mitigation": "Structure the year with internships or projects."},
                    {"point": "Hard to re-enter student mode", "severity": "medium", "mitigation": "Set re-enrollment date before leaving."},
                ],
                "alignment_score": 78,
                "priority_alignment": {"growth": 80, "financial": 45, "family_harmony": 55, "freedom": 90, "clarity": 85},
            },
            {
                "benefits": [
                    {"point": "Degree completed on schedule", "impact": "high", "reasoning": "Avoids re-enrollment friction and delays."},
                    {"point": "Peer cohort stays intact", "impact": "medium", "reasoning": "Graduate with your original class."},
                ],
                "risks": [
                    {"point": "Burnout risk remains unaddressed", "severity": "high", "mitigation": "Build recovery habits into semester routine."},
                    {"point": "Potential regret about not pausing", "severity": "medium", "mitigation": "Revisit in 6 months if stress continues."},
                ],
                "alignment_score": 65,
                "priority_alignment": {"growth": 60, "financial": 80, "family_harmony": 78, "freedom": 45, "clarity": 55},
            },
            {
                "benefits": [
                    {"point": "Earn while deciding", "impact": "medium", "reasoning": "Builds savings and real-world experience simultaneously."},
                    {"point": "Lower pressure environment", "impact": "high", "reasoning": "Work stress differs from academic stress."},
                ],
                "risks": [
                    {"point": "Harder to return to studies", "severity": "high", "mitigation": "Keep skills sharp with part-time study."},
                    {"point": "Career path delay", "severity": "medium", "mitigation": "Choose work relevant to future goals."},
                ],
                "alignment_score": 60,
                "priority_alignment": {"growth": 65, "financial": 75, "family_harmony": 60, "freedom": 80, "clarity": 70},
            },
        ],
    }

    # Fall back to general if topic not found
    general_benefits = [
        [
            {"point": "Forward momentum reduces anxiety", "impact": "high", "reasoning": "Taking action, even imperfect, breaks paralysis."},
            {"point": "Fastest path to real feedback", "impact": "high", "reasoning": "Only lived experience reveals what analysis cannot."},
        ],
        [
            {"point": "Reduces regret risk", "impact": "medium", "reasoning": "Testing before committing protects against wrong-fit."},
            {"point": "Builds evidence for decision", "impact": "medium", "reasoning": "Experiment results are more reliable than imagination."},
        ],
        [
            {"point": "Addresses hidden factors first", "impact": "high", "reasoning": "Resolving burnout or family tension before deciding leads to clearer choice."},
            {"point": "Prevents pressure-driven mistake", "impact": "medium", "reasoning": "Decisions made under duress are often regretted."},
        ],
    ]
    general_risks = [
        [
            {"point": "Irreversibility if wrong fit", "severity": "medium", "mitigation": "Set a 90-day review checkpoint."},
            {"point": "Social pressure to 'commit fully'", "severity": "low", "mitigation": "Communicate your plan clearly to key stakeholders."},
        ],
        [
            {"point": "Experiment may not give clear answer", "severity": "medium", "mitigation": "Define success criteria before starting."},
            {"point": "Delay frustration for others", "severity": "low", "mitigation": "Share timeline and milestones with family."},
        ],
        [
            {"point": "Indefinite delay risk", "severity": "high", "mitigation": "Set a hard decision deadline — max 8 weeks."},
            {"point": "Hidden factors may persist", "severity": "medium", "mitigation": "Address root cause, not just symptoms."},
        ],
    ]
    general_scores = [82, 68, 55]
    general_priority = [
        {"growth": 85, "financial": 65, "family_harmony": 60, "freedom": 80, "clarity": 75},
        {"growth": 70, "financial": 72, "family_harmony": 70, "freedom": 65, "clarity": 85},
        {"growth": 55, "financial": 78, "family_harmony": 82, "freedom": 45, "clarity": 70},
    ]

    topic_data = TRADEOFF_DATA.get(topic)
    tradeoffs = []

    for i, opt in enumerate(options):
        if topic_data and i < len(topic_data):
            d = topic_data[i]
            tradeoffs.append({
                "option_id": opt["id"],
                "option_label": opt["label"],
                "benefits": d["benefits"],
                "risks": d["risks"],
                "effort": ["medium", "low", "high"][i % 3],
                "reversibility": ["medium", "high", "low"][i % 3],
                "alignment_score": d["alignment_score"],
                "priority_alignment": d["priority_alignment"],
            })
        else:
            j = i % 3
            tradeoffs.append({
                "option_id": opt["id"],
                "option_label": opt["label"],
                "benefits": general_benefits[j],
                "risks": general_risks[j],
                "effort": ["medium", "low", "high"][j],
                "reversibility": ["medium", "high", "low"][j],
                "alignment_score": general_scores[j],
                "priority_alignment": general_priority[j],
            })

    key_tensions = {
        "abroad": [
            "Personal growth vs. family harmony",
            "Financial cost vs. career opportunity",
            "Independence now vs. stability first",
        ],
        "engineering": [
            "Sunk cost of degree vs. long-term fit",
            "Family expectations vs. personal identity",
            "Short-term pain vs. wrong-path regret",
        ],
        "gap_year": [
            "Mental health recovery vs. schedule delay",
            "Clarity gained vs. momentum lost",
            "Financial stability vs. exploration freedom",
        ],
    }.get(topic, [
        "Short-term relief vs. long-term identity",
        "Family expectations vs. personal autonomy",
        "Certainty now vs. better information later",
    ])

    return {"tradeoffs": tradeoffs, "key_tensions": key_tensions}
