# MCP server template

```bash
pip install -r requirements.txt
pytest -q
mcp dev server.py          # MCP Inspector: call tools by hand in a browser
```

Connect it to Claude Desktop: add this to `claude_desktop_config.json` and restart.
```json
{
  "mcpServers": {
    "notes": { "command": "python", "args": ["/absolute/path/to/mcp-server/server.py"] }
  }
}
```
Claude Code: `claude mcp add notes -- python /absolute/path/to/mcp-server/server.py`
