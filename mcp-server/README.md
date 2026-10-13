# MCP server template

```bash
uv sync
uv run pytest -q
uv run mcp dev notes_server.py          # MCP Inspector: call tools by hand in a browser
```

Connect it to Claude Desktop: add this to `claude_desktop_config.json` and restart.
```json
{
  "mcpServers": {
    "notes": { "command": "uv", "args": ["run", "--directory", "/absolute/path/to/mcp-server", "notes_server.py"] }
  }
}
```
Claude Code: `claude mcp add notes -- uv run --directory /absolute/path/to/mcp-server notes_server.py`
