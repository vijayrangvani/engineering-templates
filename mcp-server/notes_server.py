"""TEMPLATE: MCP server exposing tools, a resource and a prompt to any MCP client (Claude, IDEs, agents).

MCP in one line: a standard plug so ANY AI app can use YOUR functions/data without custom integration.
  tool     = action the model can call (has side effects / computes)
  resource = read-only data the client can load (like a GET)
  prompt   = reusable prompt template the user can pick
Run (stdio, how desktop clients launch it):  python notes_server.py
Debug in a browser UI:                         mcp dev notes_server.py
Note: mcp SDK v2 renamed FastMCP -> MCPServer. Older tutorials use `from mcp.server.fastmcp import FastMCP`.
"""
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("notes")               # server name shown in the client

NOTES: dict[str, str] = {}             # swap for a DB in real use


# Plain functions first (business logic, easy to unit-test), then registered with MCP below.
def add_note(title: str, body: str) -> str:
    """Save a note. Use when the user asks to remember or write something down."""
    # The docstring + type hints become the tool description/schema the MODEL reads. Write them well.
    NOTES[title] = body
    return f"saved '{title}'"


def search_notes(query: str) -> list[str]:
    """Return titles of notes whose title or body contains the query (case-insensitive)."""
    q = query.lower()
    return [t for t, b in NOTES.items() if q in t.lower() or q in b.lower()]


def read_note(title: str) -> str:
    """Full text of one note."""
    return NOTES.get(title, f"no note named '{title}'")


def weekly_review() -> str:
    """Prompt template: review all notes."""
    return "Search my notes, group them by theme, and list 3 follow-up actions."


# Registration. Same as writing @mcp.tool() above each function.
mcp.tool()(add_note)
mcp.tool()(search_notes)
mcp.resource("notes://{title}")(read_note)
mcp.prompt()(weekly_review)

if __name__ == "__main__":
    mcp.run(transport="stdio")         # desktop clients start the server and talk over stdin/stdout
