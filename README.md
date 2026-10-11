# engineering-templates

My personal cookbook of **working, line-by-line commented boilerplate**: the setup code nobody writes from memory.
Start new projects from here instead of random copy-paste, and understand every line.

| Folder | What's inside | Shape to remember |
|---|---|---|
| [`fastapi-app/`](fastapi-app) | FastAPI + SQLAlchemy 2.0 session-per-request, settings, CRUD layer, tests, Dockerfile, **Alembic migrations** ([cheat sheet](fastapi-app/MIGRATIONS.md)) | settings → engine → SessionLocal → `get_db()` (commit / rollback / close) → crud → router |
| [`auth-jwt/`](auth-jwt) | Register, login (OAuth2 form), JWT, Argon2 hashing, protected route, role check | hash on register → verify on login → token → `Depends(get_current_user)` |
| [`llm-testing/`](llm-testing) | Testable LLM code: injected client, fake client, output validation + retry, eval set with accuracy gate | parse tests → fake-client tests → real-model evals |
| [`llm-streaming/`](llm-streaming) | Token streaming with SSE + a tiny browser page (runs free without an API key) | async generator → `data: …\n\n` → `[DONE]` |
| [`mcp-server/`](mcp-server) | MCP server with tools, a resource and a prompt; Claude Desktop / Claude Code setup | `MCPServer` (SDK v2; was `FastMCP`) → `tool` / `resource` / `prompt` → `run()` |
| [`async-jobs/`](async-jobs) | Async SQLAlchemy, background jobs with polling, `asyncio.gather` | 202 + job row → background task (own session) → poll |
| [`observability/`](observability) | JSON logs, request IDs, Prometheus metrics, Prometheus + Grafana compose | middleware → log + count + time → `/metrics` |
| [`docker/`](docker) | Compose stack (API + Postgres + Redis, healthchecks, volumes), multi-stage Dockerfile | services → build/image → env → ports → volumes → depends_on → healthcheck |
| [`k8s/`](k8s) | Namespace, ConfigMap, Secret, Deployment (probes, resources), Service, Ingress, HPA | apiVersion → kind → metadata → spec |
| [`.github/workflows/`](.github/workflows) | CI: lint → test → build image (runs on this repo) | on → jobs → runs-on → steps |
| [`terraform/`](terraform) | AWS provider, S3, security group, EC2, variables, outputs | provider → resources → variables → outputs |
| [`llm/`](llm) | OpenAI + Anthropic clients, structured output, LangGraph agent with memory, Qdrant RAG | client → model → messages → call → parse |
| [`practice/`](practice) | Blank versions (shape + TODO only) with the same tests: drill writing it yourself | shape → write → test → compare |
| [`python/`](python) | Logging setup, HTTP client with retries/backoff, CLI script with argparse | — |

## How I use this repo
1. **Before copying a template:** write its *shape* from memory as comments, then compare.
2. **When copying:** change at least one value and predict what happens before running.
3. **New library?** Quickstart → run the minimal example → change one thing at a time → add a commented template here.
4. **Weekly drill:** rebuild one template from a blank file, then diff against this repo.

## Run any folder
```bash
cd <folder> && pip install -r requirements.txt && pytest -q
```

## Quick start
```bash
cd fastapi-app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest -q                          # tests
uvicorn app.main:app --reload      # http://localhost:8000/docs

cd ../docker && docker compose up -d --build   # API + Postgres + Redis
```

## Not covered yet (add when a project needs it)
Refresh tokens · Celery / arq workers · Helm · deploying from CI to a cloud
