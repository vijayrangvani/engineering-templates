# engineering-templates

My personal cookbook of **working, line-by-line commented boilerplate**: the setup code nobody writes from memory.
Start new projects from here instead of random copy-paste, and understand every line.

| Folder | What's inside | Shape to remember |
|---|---|---|
| [`fastapi-app/`](fastapi-app) | FastAPI + SQLAlchemy 2.0 session-per-request, settings, CRUD layer, tests, Dockerfile | settings → engine → SessionLocal → `get_db()` (commit / rollback / close) → crud → router |
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

## Not covered yet (add as I learn)
Alembic migrations · JWT auth · async SQLAlchemy · Celery / background jobs · Prometheus metrics · Helm
