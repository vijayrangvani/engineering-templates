import asyncio

import notes_server as server


def setup_function():
    server.NOTES.clear()


def test_tool_logic():
    # Logic lives in plain functions -> test it directly, no MCP client needed.
    server.add_note("groceries", "milk, eggs")
    assert server.search_notes("MILK") == ["groceries"]
    assert server.read_note("groceries") == "milk, eggs"


def test_tools_are_registered():
    result = asyncio.run(server.mcp.list_tools())
    tools = getattr(result, "tools", result)       # list result (some SDK versions wrap it)
    assert {"add_note", "search_notes"} <= {t.name for t in tools}
