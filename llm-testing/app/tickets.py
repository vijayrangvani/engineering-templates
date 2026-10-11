"""TEMPLATE: LLM code written to be TESTABLE.

Key idea: the LLM client is passed in (dependency injection), never created inside the function.
Tests pass a fake client -> no API key, no cost, deterministic, fast.
"""
import json

from pydantic import BaseModel, Field, ValidationError

CATEGORIES = ["billing", "technical", "account", "other"]

SYSTEM_PROMPT = (
    "Classify the support ticket. Reply with JSON only: "
    '{"category": one of ' + json.dumps(CATEGORIES) + ', "priority": 1-5, "summary": "<= 15 words"}'
)


class Ticket(BaseModel):
    category: str
    priority: int = Field(ge=1, le=5)
    summary: str


class LLMOutputError(Exception):
    """The model returned something we couldn't use."""


def parse_ticket(raw: str) -> Ticket:
    """Pure function: string in, validated object out. The easiest part to test thoroughly."""
    raw = raw.strip().removeprefix("```json").removesuffix("```").strip()  # models love code fences
    try:
        ticket = Ticket.model_validate_json(raw)
    except ValidationError as e:
        raise LLMOutputError(f"invalid output: {raw[:100]}") from e
    if ticket.category not in CATEGORIES:
        raise LLMOutputError(f"unknown category: {ticket.category}")
    return ticket


def classify(client, text: str, model: str = "gpt-4o-mini", retries: int = 1) -> Ticket:
    """`client` = anything with .chat.completions.create(...) -> real OpenAI() or a fake in tests."""
    if not text.strip():
        raise ValueError("empty ticket")
    last_error = None
    for _ in range(retries + 1):              # one retry on bad output is a common, cheap fix
        resp = client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
        )
        try:
            return parse_ticket(resp.choices[0].message.content)
        except LLMOutputError as e:
            last_error = e
    raise last_error
