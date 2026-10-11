import json

from fastapi.testclient import TestClient

from app.main import app


def test_stream_sends_tokens_then_done(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)     # force the fake model
    client = TestClient(app)
    with client.stream("GET", "/chat/stream", params={"q": "hi"}) as r:
        assert r.headers["content-type"].startswith("text/event-stream")
        events = [line[len("data: "):] for line in r.iter_lines() if line.startswith("data: ")]
    assert events[-1] == "[DONE]"
    text = "".join(json.loads(e)["token"] for e in events[:-1])
    assert "You asked: hi" in text


def test_empty_question_rejected():
    assert TestClient(app).get("/chat/stream", params={"q": ""}).status_code == 422
