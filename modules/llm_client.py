"""OpenAI client wrapper with structured JSON responses."""

from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_client() -> OpenAI | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-your"):
        return None
    return OpenAI(api_key=api_key)


def call_llm_json(
    system_prompt: str,
    user_prompt: str,
    *,
    model: str | None = None,
) -> dict[str, Any]:
    """Call OpenAI and parse a JSON object response."""
    client = get_client()
    if client is None:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to a .env file or use Demo Mode."
        )

    response = client.chat.completions.create(
        model=model or DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
    )
    content = response.choices[0].message.content or "{}"
    return json.loads(content)
