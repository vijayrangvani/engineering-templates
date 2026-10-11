import asyncio

import server


def setup_function():
    server.NOTES.clear()


def test_tools_are_plain_functions():
    # The decorators register the function and return it unchanged -> unit-test directly.
    server.add_note("groceries", "milk, eggs")
    assert server.search_notes("MILK") == ["groceries"]
    assert server.read_note("groceries") == "milk, eggs"


def test_tools_are_registered_with_schemas():
    tools = {t.name: t for t in asyncio.run(server.mcp.list_tools())}
    assert {"add_note", "search_notes"} <= set(tools)
    assert "title" in tools["add_note"].inputSchema["properties"]   # built from type hints
