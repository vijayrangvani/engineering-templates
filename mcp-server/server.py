"""TEMPLATE: MCP server exposing tools, a resource and a prompt to any MCP client (Claude, IDEs, agents).

MCP in one line: a standard plug so ANY AI app can use YOUR functions/data without custom integration.
  tool     = action the model can call (has side effects / computes)
  resource = read-only data the client can load (like a GET)
  prompt   = reusable prompt template the user can pick
Run (stdio, how desktop clients launch it):  python server.py
Debug in a browser UI:                         mcp dev server.py
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notes")                 # server name shown in the client

NOTES: dict[str, str] = {}             # swap for a DB in real use


@mcp.tool()
def add_note(title: str, body: str) -> str:
    """Save a note. Use when the user asks to remember or write something down."""
    # The docstring + type hints become the tool description/schema the MODEL reads. Write them well.
    NOTES[title] = body
    return f"saved '{title}'"


@mcp.tool()
def search_notes(query: str) -> list[str]:
    """Return titles of notes whose title or body contains the query (case-insensitive)."""
    q = query.lower()
    return [t for t, b in NOTES.items() if q in t.lower() or q in b.lower()]


@mcp.resource("notes://{title}")
def read_note(title: str) -> str:
    """Full text of one note."""
    return NOTES.get(title, f"no note named '{title}'")


@mcp.prompt()
def weekly_review() -> str:
    """Prompt template: review all notes."""
    return "Search my notes, group them by theme, and list 3 follow-up actions."


if __name__ == "__main__":
    mcp.run()                          # default transport: stdio
