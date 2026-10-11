"""TEMPLATE: evaluation = run the REAL model on a labelled set and measure accuracy.

Unit tests prove your code works; evals prove the model + prompt work. Run after every prompt/model change.
Run from llm-testing/:  OPENAI_API_KEY=... python -m evals.run_eval --model gpt-4o-mini
"""
import argparse
import json
from pathlib import Path

from openai import OpenAI

from app.tickets import LLMOutputError, classify

DATASET = Path(__file__).parent / "dataset.jsonl"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="gpt-4o-mini")
    p.add_argument("--min-accuracy", type=float, default=0.8)   # quality gate
    args = p.parse_args()

    client = OpenAI()
    rows = [json.loads(line) for line in DATASET.read_text().splitlines() if line.strip()]
    correct = 0
    for row in rows:
        try:
            got = classify(client, row["text"], model=args.model).category
        except LLMOutputError:
            got = "<invalid>"
        ok = got == row["category"]
        correct += ok
        print(f"{'PASS' if ok else 'FAIL'}  expected={row['category']:<10} got={got:<10} {row['text'][:50]}")
    accuracy = correct / len(rows)
    print(f"\naccuracy: {accuracy:.0%} ({correct}/{len(rows)})")
    if accuracy < args.min_accuracy:
        raise SystemExit(f"below gate {args.min_accuracy:.0%}")   # non-zero exit -> CI can block


if __name__ == "__main__":
    main()
