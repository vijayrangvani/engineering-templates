"""A fake OpenAI client: same shape (.chat.completions.create -> .choices[0].message.content).

Returns scripted replies in order and records every call so tests can inspect prompts.
"""
from types import SimpleNamespace


class FakeLLM:
    def __init__(self, *replies: str):
        self.replies = list(replies)
        self.calls: list[dict] = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        content = self.replies.pop(0)
        message = SimpleNamespace(content=content)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])
