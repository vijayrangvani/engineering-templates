"""TEMPLATE: stream LLM tokens to the browser with Server-Sent Events (SSE).

Why: users see text appear immediately instead of waiting 10s for the full answer.
SSE format: each message is `data: <payload>\n\n`; the browser's EventSource reads it.
Run: uvicorn app.main:app --reload -> open http://localhost:8000
Without OPENAI_API_KEY it streams a fake answer, so you can run it for free.
"""
import asyncio
import json
import os
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI(title="llm-streaming")


async def openai_tokens(prompt: str) -> AsyncIterator[str]:
    from openai import AsyncOpenAI

    client = AsyncOpenAI()
    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True,                       # server sends chunks as they're generated
    )
    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:   # some chunks carry no text
            yield chunk.choices[0].delta.content


async def fake_tokens(prompt: str) -> AsyncIterator[str]:
    for word in f"(fake model) You asked: {prompt}. Streaming works!".split():
        await asyncio.sleep(0.05)          # simulate generation time
        yield word + " "


async def sse_events(prompt: str) -> AsyncIterator[str]:
    source = openai_tokens if os.getenv("OPENAI_API_KEY") else fake_tokens
    try:
        async for token in source(prompt):
            yield f"data: {json.dumps({'token': token})}\n\n"   # JSON keeps newlines/quotes safe
    except Exception as e:                 # headers are already sent: report errors IN the stream
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
    yield "data: [DONE]\n\n"               # tell the client to stop listening


@app.get("/chat/stream")
async def chat_stream(q: Annotated[str, Query(min_length=1, max_length=2000)]):
    return StreamingResponse(
        sse_events(q),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},  # stop nginx buffering
    )


PAGE = """<!doctype html><meta charset="utf-8"><title>stream</title>
<input id="q" value="Explain SSE in one line" size="50"><button onclick="go()">Ask</button>
<pre id="out" style="white-space:pre-wrap"></pre>
<script>
function go() {
  const out = document.getElementById("out"); out.textContent = "";
  const es = new EventSource("/chat/stream?q=" + encodeURIComponent(document.getElementById("q").value));
  es.onmessage = (e) => {
    if (e.data === "[DONE]") return es.close();
    const msg = JSON.parse(e.data);
    out.textContent += msg.token ?? ("\\n[error] " + msg.error);
  };
}
</script>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return PAGE
