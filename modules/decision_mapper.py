"""Module 3 — Decision mapper: build a decision tree of options."""

from __future__ import annotations

import json
from typing import Any

from modules.llm_client import call_llm_json

SYSTEM_PROMPT = """You are PathERA's Decision Mapper.
Given a user's dilemma and analyzed context, build a decision tree of realistic options.

Return JSON:
{
  "root_question": "the core decision in one question",
  "options": [
    {
      "id": "opt_1",
      "label": "short option name",
      "description": "what this path entails",
      "prerequisites": ["what must be true or done first"],
      "sub_options": [
        {"id": "opt_1a", "label": "variant or next fork", "description": "detail"}
      ]
    }
  ],
  "tree_edges": [
    {"from": "root", "to": "opt_1", "label": "choose path"},
    {"from": "opt_1", "to": "opt_1a", "label": "if..."}
  ]
}

Provide 3-5 main options with 1-2 sub-options each where branching makes sense."""


def map_decisions(user_input: str, context: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps({"dilemma": user_input, "context": context}, indent=2)
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


def demo_decisions(user_input: str, context: dict[str, Any]) -> dict[str, Any]:
    topic = _detect_topic(user_input)

    if topic == "engineering":
        return {
            "root_question": "Should you leave engineering — and if so, how?",
            "options": [
                {
                    "id": "opt_stay",
                    "label": "Stay & recalibrate",
                    "description": "Reduce load, change specialization, or take a semester break.",
                    "prerequisites": ["Talk to academic advisor", "Assess burnout severity"],
                    "sub_options": [
                        {"id": "opt_stay_spec", "label": "Switch specialization", "description": "Move within engineering (e.g. CS → product design)"},
                        {"id": "opt_stay_break", "label": "Planned break", "description": "1 semester off with a return plan"},
                    ],
                },
                {
                    "id": "opt_pivot",
                    "label": "Pivot adjacent field",
                    "description": "Leverage partial degree into tech-adjacent roles (PM, UX, data).",
                    "prerequisites": ["Identify transferable credits", "Build portfolio projects"],
                    "sub_options": [],
                },
                {
                    "id": "opt_leave",
                    "label": "Leave engineering",
                    "description": "Exit degree and pursue a different path entirely.",
                    "prerequisites": ["Financial runway plan", "Skills audit"],
                    "sub_options": [
                        {"id": "opt_leave_study", "label": "New degree/program", "description": "Start fresh in another discipline"},
                        {"id": "opt_leave_work", "label": "Enter workforce", "description": "Job + upskilling route"},
                    ],
                },
            ],
            "tree_edges": [
                {"from": "root", "to": "opt_stay", "label": "not ready to quit"},
                {"from": "root", "to": "opt_pivot", "label": "partial fit"},
                {"from": "root", "to": "opt_leave", "label": "clear misalignment"},
                {"from": "opt_stay", "to": "opt_stay_spec", "label": "still curious"},
                {"from": "opt_stay", "to": "opt_stay_break", "label": "need recovery"},
                {"from": "opt_leave", "to": "opt_leave_study", "label": "formal retraining"},
                {"from": "opt_leave", "to": "opt_leave_work", "label": "earn while exploring"},
            ],
        }

    if topic == "abroad":
        return {
            "root_question": "How and when should you pursue studying abroad?",
            "options": [
                {
                    "id": "opt_apply_now",
                    "label": "Apply this year",
                    "description": "Commit to the process now — research programs, prepare documents, apply.",
                    "prerequisites": ["Shortlist 3 programs", "Check visa requirements", "Discuss finances with family"],
                    "sub_options": [
                        {"id": "opt_apply_full", "label": "Full degree abroad", "description": "Transfer or enroll in a complete overseas program"},
                        {"id": "opt_apply_exchange", "label": "Exchange semester", "description": "1-2 semesters abroad through your current university"},
                    ],
                },
                {
                    "id": "opt_apply_next",
                    "label": "Prepare & apply next year",
                    "description": "Spend this year strengthening your application and saving money.",
                    "prerequisites": ["Set savings target", "Improve language/test scores if needed"],
                    "sub_options": [],
                },
                {
                    "id": "opt_local",
                    "label": "Study locally for now",
                    "description": "Build credentials locally first, revisit abroad in 2 years.",
                    "prerequisites": ["Research local programs", "Talk honestly with family about long-term goals"],
                    "sub_options": [
                        {"id": "opt_local_remote", "label": "Remote international programs", "description": "Online courses from foreign universities while staying local"},
                    ],
                },
            ],
            "tree_edges": [
                {"from": "root", "to": "opt_apply_now", "label": "ready to commit"},
                {"from": "root", "to": "opt_apply_next", "label": "need more prep"},
                {"from": "root", "to": "opt_local", "label": "family/financial barriers"},
                {"from": "opt_apply_now", "to": "opt_apply_full", "label": "full commitment"},
                {"from": "opt_apply_now", "to": "opt_apply_exchange", "label": "lower risk test"},
                {"from": "opt_local", "to": "opt_local_remote", "label": "compromise path"},
            ],
        }

    if topic == "gap_year":
        return {
            "root_question": "Should you take a gap year — and how do you structure it?",
            "options": [
                {
                    "id": "opt_gap_structured",
                    "label": "Structured gap year",
                    "description": "Take time off with a clear plan — internship, project, travel with purpose.",
                    "prerequisites": ["Define 3 goals for the year", "Secure at least one anchor activity"],
                    "sub_options": [
                        {"id": "opt_gap_intern", "label": "Internship-focused", "description": "Work in target industry to test fit"},
                        {"id": "opt_gap_build", "label": "Build something", "description": "Personal project, startup, or portfolio"},
                    ],
                },
                {
                    "id": "opt_push_through",
                    "label": "Push through & finish",
                    "description": "Stay enrolled but build better coping and recovery habits.",
                    "prerequisites": ["Talk to counselor about burnout", "Reduce non-essential commitments"],
                    "sub_options": [],
                },
                {
                    "id": "opt_semester_off",
                    "label": "Take one semester off",
                    "description": "Smaller pause — work or rest, then return with a clear re-entry plan.",
                    "prerequisites": ["Confirm leave of absence policy", "Set re-enrollment date before leaving"],
                    "sub_options": [],
                },
            ],
            "tree_edges": [
                {"from": "root", "to": "opt_gap_structured", "label": "need a full reset"},
                {"from": "root", "to": "opt_push_through", "label": "stay on track"},
                {"from": "root", "to": "opt_semester_off", "label": "small pause"},
                {"from": "opt_gap_structured", "to": "opt_gap_intern", "label": "career clarity"},
                {"from": "opt_gap_structured", "to": "opt_gap_build", "label": "build portfolio"},
            ],
        }

    if topic == "career":
        return {
            "root_question": "How should you navigate this career decision?",
            "options": [
                {
                    "id": "opt_take_it",
                    "label": "Accept & commit",
                    "description": "Take the opportunity and give it full effort for at least 6 months.",
                    "prerequisites": ["Negotiate terms if needed", "Set 90-day success metrics"],
                    "sub_options": [],
                },
                {
                    "id": "opt_negotiate",
                    "label": "Negotiate before deciding",
                    "description": "Push for better terms — role scope, timeline, or compensation.",
                    "prerequisites": ["Know your minimum acceptable terms", "Research market rates"],
                    "sub_options": [],
                },
                {
                    "id": "opt_explore_more",
                    "label": "Keep exploring first",
                    "description": "Run more interviews or experiments before committing.",
                    "prerequisites": ["Set a decision deadline", "Define what a better option looks like"],
                    "sub_options": [],
                },
            ],
            "tree_edges": [
                {"from": "root", "to": "opt_take_it", "label": "strong fit"},
                {"from": "root", "to": "opt_negotiate", "label": "good but not right terms"},
                {"from": "root", "to": "opt_explore_more", "label": "not convinced yet"},
            ],
        }

    # General fallback
    return {
        "root_question": "What is your best next move given your goals and constraints?",
        "options": [
            {
                "id": "opt_a",
                "label": "Commit to primary path",
                "description": "Move forward with the option you're most drawn to.",
                "prerequisites": ["Validate assumptions with 2 conversations"],
                "sub_options": [],
            },
            {
                "id": "opt_b",
                "label": "Explore before deciding",
                "description": "Run a 4-8 week low-risk experiment (internship, course, shadowing).",
                "prerequisites": ["Define success criteria for the experiment"],
                "sub_options": [],
            },
            {
                "id": "opt_c",
                "label": "Delay & gather data",
                "description": "Buy time while addressing hidden factors (burnout, family talks).",
                "prerequisites": ["Set a decision deadline"],
                "sub_options": [],
            },
        ],
        "tree_edges": [
            {"from": "root", "to": "opt_a", "label": "high conviction"},
            {"from": "root", "to": "opt_b", "label": "need evidence"},
            {"from": "root", "to": "opt_c", "label": "not ready yet"},
        ],
    }
