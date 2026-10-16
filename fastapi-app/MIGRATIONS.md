# Alembic cheat sheet

Why: `Base.metadata.create_all()` only creates *missing* tables. It never adds a column to an
existing table. Migrations are versioned, reviewable schema changes you can apply and undo.

```bash
alembic upgrade head                              # apply all migrations (run on deploy)
alembic revision --autogenerate -m "add sku"      # 1. change models.py  2. generate diff
#   -> OPEN the new file in migrations/versions/ and check it (autogenerate misses renames!)
alembic upgrade head                              # 3. apply
alembic downgrade -1                              # undo the last one
alembic current / alembic history                 # where am I / list
alembic check                                     # fails if models and migrations differ (used in CI)
```

Rules:
- Never edit a migration that's already applied on a shared DB. Write a new one.
- Commit migrations with the model change in the same PR.
- The app does NOT create tables on startup: run `alembic upgrade head` first, locally too.
- In production, run it as a deploy step: the `migrate` service in `docker/docker-compose.yml`, or `k8s/07-migrate-job.yaml`.
