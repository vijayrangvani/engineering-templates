"""TEMPLATE: calling LLM APIs (OpenAI + Anthropic) with the same shape.

Shape: client (key from env) -> model -> messages -> call -> read text -> handle errors.
Run:  python llm_clients.py   (needs OPENAI_API_KEY and/or ANTHROPIC_API_KEY in env or .env)
"""
import os

from dotenv import load_dotenv

load_dotenv()  # read .env into environment variables (dev convenience)


def ask_openai(question: str, model: str = "gpt-4o-mini") -> str:
    from openai import OpenAI

    client = OpenAI()  # reads OPENAI_API_KEY automatically; also has timeout/max_retries args
    resp = client.chat.completions.create(
        model=model,
        temperature=0.2,  # low = more deterministic
        messages=[
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": question},
        ],
    )
    return resp.choices[0].message.content


def ask_anthropic(question: str, model: str = "claude-haiku-4-5") -> str:
    import anthropic

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    resp = client.messages.create(
        model=model,
        max_tokens=500,  # REQUIRED for Anthropic
        system="You are a concise assistant.",  # system prompt is a separate arg, not a message
        messages=[{"role": "user", "content": question}],
    )
    return resp.content[0].text  # content is a list of blocks


if __name__ == "__main__":
    q = "Explain a database connection pool in 2 sentences."
    if os.getenv("OPENAI_API_KEY"):
        print("OpenAI:", ask_openai(q))
    if os.getenv("ANTHROPIC_API_KEY"):
        print("Anthropic:", ask_anthropic(q))
