"""Module 5 — Scenario simulator: likely challenges and outcomes per path."""

from __future__ import annotations

import json
from typing import Any

from modules.llm_client import call_llm_json

SYSTEM_PROMPT = """You are PathERA's Scenario Simulator — the star feature.
For each decision option, simulate plausible futures: challenges → responses → outcomes.

Return JSON:
{
  "scenarios": [
    {
      "option_id": "id",
      "option_label": "name",
      "timeline": "6 months|1 year|3 years",
      "narrative": "2-3 sentence story of what life might look like",
      "challenges": [
        {"challenge": "what goes wrong or gets hard", "probability": "low|medium|high", "coping": "how user might handle it"}
      ],
      "positive_outcomes": ["likely good results if user adapts well"],
      "negative_outcomes": ["realistic downsides"],
      "confidence": "low|medium|high"
    }
  ],
  "wildcard": {
    "insight": "one non-obvious pattern across scenarios",
    "blind_spot": "what the user may be underestimating"
  }
}"""


def simulate_scenarios(
    user_input: str,
    context: dict[str, Any],
    decision_tree: dict[str, Any],
    tradeoffs: dict[str, Any],
) -> dict[str, Any]:
    payload = json.dumps(
        {"dilemma": user_input, "context": context, "decision_tree": decision_tree, "tradeoffs": tradeoffs},
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


def demo_scenarios(
    user_input: str,
    context: dict[str, Any],
    decision_tree: dict[str, Any],
    tradeoffs: dict[str, Any],
) -> dict[str, Any]:
    topic = _detect_topic(user_input)
    options = decision_tree.get("options", [])

    SCENARIO_DATA = {
        "abroad": [
            {
                "timeline": "1 year",
                "narrative": "You land in a new country with your acceptance letter and a mix of excitement and homesickness. The first semester is hard — unfamiliar systems, a new language, and no local support network. By month 8, you've built real friendships and your confidence has visibly shifted.",
                "challenges": [
                    {"challenge": "Visa delays and paperwork stress", "probability": "high", "coping": "Start applications 6 months early; use university's international office."},
                    {"challenge": "Homesickness and isolation in first 3 months", "probability": "high", "coping": "Join 2+ student clubs in week one — connection is the cure."},
                    {"challenge": "Higher living costs than expected", "probability": "medium", "coping": "Track spending weekly; apply for on-campus work permit."},
                ],
                "positive_outcomes": ["Strong international network built", "Career confidence and independence", "Language or cultural skills added to resume"],
                "negative_outcomes": ["Financial strain if funding falls short", "Family relationship tension during adjustment period"],
            },
            {
                "timeline": "1 year",
                "narrative": "You spend this year doing research, talking to alumni, and strengthening your application. It feels slow at times — watching peers move forward while you wait. But by year-end, you have a shortlist of programs and a clearer sense of what you actually want.",
                "challenges": [
                    {"challenge": "FOMO watching peers move ahead", "probability": "high", "coping": "Track your own milestones, not others' timelines."},
                    {"challenge": "Family pressure to 'just decide'", "probability": "medium", "coping": "Show them your structured preparation plan."},
                ],
                "positive_outcomes": ["Stronger application and clearer program fit", "Financial savings during prep year", "Reduced anxiety from having a concrete plan"],
                "negative_outcomes": ["Risk of perpetual preparation without action", "1 year delay in international exposure"],
            },
            {
                "timeline": "1 year",
                "narrative": "You stay local, enroll in a strong program near home, and build your resume. Family relationships stay smooth. At times you wonder 'what if' — but you're making real progress and carrying less financial stress than your peers abroad.",
                "challenges": [
                    {"challenge": "Lingering 'what if abroad' regret", "probability": "medium", "coping": "Revisit the abroad option in 2 years with stronger credentials."},
                    {"challenge": "Fewer international connections", "probability": "medium", "coping": "Attend global conferences and online communities."},
                ],
                "positive_outcomes": ["Debt-free or low-debt graduation", "Strong family support during studies", "Local network and internship access"],
                "negative_outcomes": ["Fewer global career doors in short term", "Possible long-term regret if abroad was the real goal"],
            },
        ],
        "engineering": [
            {
                "timeline": "1 year",
                "narrative": "You switch specialization or reduce your load. The first semester feels like relief — the specific pressure that was suffocating you lifts. You're not fully healed, but you're curious again about at least parts of your field.",
                "challenges": [
                    {"challenge": "Adjustment period in new specialization", "probability": "medium", "coping": "Give it one full semester before judging — new things feel hard first."},
                    {"challenge": "Catching up on new subject requirements", "probability": "medium", "coping": "Use summer to cover prerequisites; ask seniors for notes."},
                ],
                "positive_outcomes": ["Burnout reduces significantly", "Degree stays on track", "New area may reignite genuine interest"],
                "negative_outcomes": ["May discover new area also isn't right fit", "Slight delay in graduation timeline"],
            },
            {
                "timeline": "1 year",
                "narrative": "You finish your degree but redirect your energy toward product, data, or design. You're building a portfolio while still in school. Interviews feel different — you're pitching a story, not just grades.",
                "challenges": [
                    {"challenge": "Imposter syndrome in non-engineering spaces", "probability": "high", "coping": "Your technical background is actually a superpower in most adjacent fields."},
                    {"challenge": "Building portfolio while finishing coursework", "probability": "medium", "coping": "One project per semester is enough — quality over quantity."},
                ],
                "positive_outcomes": ["Engineering + adjacent skills combo is rare and valuable", "Clear career narrative by graduation", "Higher job satisfaction in aligned role"],
                "negative_outcomes": ["Transition takes longer than expected", "Some peers don't understand the pivot"],
            },
            {
                "timeline": "1 year",
                "narrative": "You leave. The first few months feel like freedom mixed with panic. No more exams you dread — but also no clear path yet. By month 6, you're either building something new or deeply regretting the leap without a plan.",
                "challenges": [
                    {"challenge": "Loss of student identity and structure", "probability": "high", "coping": "Build a daily routine immediately — structure reduces anxiety."},
                    {"challenge": "Family and financial pressure", "probability": "high", "coping": "Have an honest conversation and a 6-month financial plan before leaving."},
                ],
                "positive_outcomes": ["Full alignment between daily work and genuine interest", "Freedom to pursue what actually excites you"],
                "negative_outcomes": ["High financial and emotional cost without a plan", "May take 2+ years to find stable footing"],
            },
        ],
        "gap_year": [
            {
                "timeline": "1 year",
                "narrative": "You take the gap year. The first month is disorienting — the structure of school disappears and you feel unmoored. By month 4, you're either building something real or slipping into drift. The outcome depends entirely on whether you fill the year with purpose.",
                "challenges": [
                    {"challenge": "Loss of academic structure and routine", "probability": "high", "coping": "Design your own schedule in week one — treat it like a job."},
                    {"challenge": "Social isolation from peers still in school", "probability": "medium", "coping": "Find gap year communities or work alongside people with similar goals."},
                ],
                "positive_outcomes": ["Mental health recovery and restored motivation", "Real-world clarity that no classroom provides", "Stronger sense of direction when you return"],
                "negative_outcomes": ["Risk of drift without structured goals", "Resume gap if year is unproductive"],
            },
            {
                "timeline": "1 year",
                "narrative": "You push through. The burnout is still there in week one — but you build coping strategies. By semester 2, you've found a rhythm. Not every day is good, but you're moving forward and your degree stays on track.",
                "challenges": [
                    {"challenge": "Burnout resurfacing under exam pressure", "probability": "high", "coping": "Build weekly recovery habits — exercise, sleep, and one non-study hobby."},
                    {"challenge": "Motivation dips mid-semester", "probability": "medium", "coping": "Break semester into 4-week sprints with small rewards."},
                ],
                "positive_outcomes": ["Degree completed on schedule", "Peers and professors relationship maintained", "Proves to yourself you can manage difficulty"],
                "negative_outcomes": ["Chronic stress if root cause isn't addressed", "Quality of work may suffer under strain"],
            },
            {
                "timeline": "1 year",
                "narrative": "You take a semester off and work. It's humbling at first — but earning money and being in the real world reframes everything. Academic problems feel smaller from the outside. Many students return with sharper focus.",
                "challenges": [
                    {"challenge": "Re-adjustment to student life after working", "probability": "medium", "coping": "Stay connected to university community during leave."},
                    {"challenge": "Falling behind on coursework momentum", "probability": "medium", "coping": "Review syllabi and keep skills sharp with self-study."},
                ],
                "positive_outcomes": ["Financial buffer and real-world perspective", "Academic reset and renewed motivation", "Stronger clarity on whether degree is actually worth finishing"],
                "negative_outcomes": ["Harder to return than expected", "Peer cohort moves ahead by one semester"],
            },
        ],
    }

    general_scenarios = [
        {
            "timeline": "1 year",
            "narrative": "You commit and move. The first weeks feel exposing — no more 'deciding' to hide behind, just doing. Most of the fears you had don't materialise. The ones that do, you handle better than expected.",
            "challenges": [
                {"challenge": "Early results don't match expectations", "probability": "medium", "coping": "Track leading indicators, not just outcomes — effort counts."},
                {"challenge": "Second-guessing once committed", "probability": "high", "coping": "Remind yourself why you chose this — write it down before you start."},
            ],
            "positive_outcomes": ["Clarity that only comes from action", "Confidence from following through on hard decision", "Real feedback to refine your path"],
            "negative_outcomes": ["Path may need adjustment after real-world test", "Short-term discomfort during transition"],
        },
        {
            "timeline": "1 year",
            "narrative": "You design a 6-week experiment. It's lower stakes than a full commitment, which makes it easier to start honestly. By the end, you have real data — not imagined fears or hopes.",
            "challenges": [
                {"challenge": "Experiment feels inconclusive", "probability": "medium", "coping": "Define what 'good enough signal' looks like before you start."},
                {"challenge": "Others pressure you to 'just decide'", "probability": "medium", "coping": "Explain your method — structured experiments are more rational, not less."},
            ],
            "positive_outcomes": ["Evidence-based decision reduces regret", "Low-cost way to test a high-stakes choice", "Confidence that you explored properly"],
            "negative_outcomes": ["May extend uncertainty period", "Some doors require full commitment to open"],
        },
        {
            "timeline": "1 year",
            "narrative": "You buy time deliberately. You address the hidden factors — burnout, family tension, information gaps. After 8 weeks you feel clearer. The decision hasn't changed, but your relationship to it has.",
            "challenges": [
                {"challenge": "Delay becomes default rather than tool", "probability": "high", "coping": "Set a non-negotiable decision date 8 weeks out."},
                {"challenge": "Hidden factors harder to resolve than expected", "probability": "medium", "coping": "Address the biggest one first — progress on one unlocks others."},
            ],
            "positive_outcomes": ["Clearer head leads to better decision", "Hidden factors addressed instead of carried forward", "Reduced anxiety from having a structured pause"],
            "negative_outcomes": ["Opportunity cost if delay is too long", "Others may lose patience or move on without you"],
        },
    ]

    topic_data = SCENARIO_DATA.get(topic)
    scenarios = []

    for i, opt in enumerate(options):
        if topic_data and i < len(topic_data):
            d = topic_data[i]
            scenarios.append({
                "option_id": opt["id"],
                "option_label": opt["label"],
                "timeline": d["timeline"],
                "narrative": d["narrative"],
                "challenges": d["challenges"],
                "positive_outcomes": d["positive_outcomes"],
                "negative_outcomes": d["negative_outcomes"],
                "confidence": "medium",
            })
        else:
            j = i % 3
            g = general_scenarios[j]
            scenarios.append({
                "option_id": opt["id"],
                "option_label": opt["label"],
                "timeline": g["timeline"],
                "narrative": g["narrative"],
                "challenges": g["challenges"],
                "positive_outcomes": g["positive_outcomes"],
                "negative_outcomes": g["negative_outcomes"],
                "confidence": "medium",
            })

    wildcards = {
        "abroad": {
            "insight": "Students who go abroad often report the hardest part wasn't the academics — it was the identity shift. Plan for that, not just the logistics.",
            "blind_spot": "The family resistance you're anticipating may soften significantly once they see you have a real plan.",
        },
        "engineering": {
            "insight": "Most people who 'quit engineering' don't leave tech — they find a better fit within it. The field is wider than your current course suggests.",
            "blind_spot": "Burnout and wrong-fit feel identical from the inside. Your decision will be much clearer after 2 weeks of genuine rest.",
        },
        "gap_year": {
            "insight": "The students who benefit most from gap years are the ones who treat it like a job — structured, goal-driven, with clear milestones.",
            "blind_spot": "You may be underestimating how hard it is to re-enter academic mode. Build a re-entry plan before you leave.",
        },
    }

    wildcard = wildcards.get(topic, {
        "insight": "Your strongest path may be the one that lets you test assumptions fastest — not the one that feels safest right now.",
        "blind_spot": context.get("hidden_factors", [{}])[0].get("factor", "The emotional cost of staying undecided is higher than either path."),
    })

    return {"scenarios": scenarios, "wildcard": wildcard}
