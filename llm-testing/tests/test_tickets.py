"""TEMPLATE: 3 layers of LLM tests.
1. Pure parsing/validation (no LLM at all)   2. Logic around the LLM (fake client)
3. Real model quality (evals/, run separately, costs money)
"""
from unittest.mock import MagicMock

import pytest

from app.tickets import LLMOutputError, classify, parse_ticket
from tests.fakes import FakeLLM

GOOD = '{"category": "billing", "priority": 4, "summary": "Charged twice"}'


# ---- 1. parsing ----
def test_parse_valid():
    assert parse_ticket(GOOD).category == "billing"


def test_parse_strips_code_fence():
    assert parse_ticket(f"```json\n{GOOD}\n```").priority == 4


@pytest.mark.parametrize("raw", [
    "not json",
    '{"category": "billing"}',                                        # missing fields
    '{"category": "billing", "priority": 9, "summary": "x"}',         # out of range
    '{"category": "weather", "priority": 1, "summary": "x"}',         # unknown category
])
def test_parse_rejects_bad_output(raw):
    with pytest.raises(LLMOutputError):
        parse_ticket(raw)


# ---- 2. logic with a fake client ----
def test_classify_sends_ticket_and_system_prompt():
    llm = FakeLLM(GOOD)
    classify(llm, "I was charged twice")
    sent = llm.calls[0]
    assert sent["temperature"] == 0
    assert sent["messages"][0]["role"] == "system"
    assert sent["messages"][1]["content"] == "I was charged twice"


def test_classify_retries_once_on_bad_output():
    llm = FakeLLM("garbage", GOOD)
    assert classify(llm, "charged twice").category == "billing"
    assert len(llm.calls) == 2


def test_classify_gives_up_after_retries():
    with pytest.raises(LLMOutputError):
        classify(FakeLLM("garbage", "still garbage"), "charged twice")


def test_empty_ticket_never_calls_llm():
    llm = MagicMock()                 # MagicMock: alternative to a hand-written fake
    with pytest.raises(ValueError):
        classify(llm, "   ")
    llm.chat.completions.create.assert_not_called()
