"""TEMPLATE: a script with arguments, logging, and a main() guard.

Run: python cli_script.py data.csv --limit 5 --verbose
"""
import argparse
import csv
import logging
import sys
from pathlib import Path

log = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Print the first rows of a CSV file.")
    p.add_argument("path", type=Path, help="CSV file to read")                  # positional, required
    p.add_argument("--limit", type=int, default=10, help="rows to print")        # optional with default
    p.add_argument("-v", "--verbose", action="store_true", help="debug logging") # flag
    return p.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    if not args.path.exists():
        log.error("file not found: %s", args.path)
        return 1                                   # non-zero exit code = failure (CI / shell can detect it)
    with args.path.open(newline="", encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f)):  # rows as dicts keyed by header
            if i >= args.limit:
                break
            print(row)
    log.debug("done")
    return 0


if __name__ == "__main__":                         # runs only when executed, not when imported
    sys.exit(main())
