# TEMPLATE: production Dockerfile for a Python API, using uv.
# Shape: base -> uv -> env -> workdir -> deps (cached layer, from the lock) -> code -> non-root user -> port -> start

# Slim official image; keep the version equal to .python-version.
FROM python:3.14-slim

# uv binary from its official image (pinned version, no pip needed).
COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /bin/uv

# No .pyc at runtime; logs go straight to stdout; uv pre-compiles bytecode at install time.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Copy ONLY the dependency files first: this layer is cached until pyproject.toml / uv.lock change,
# so code edits don't trigger a full reinstall. --locked = fail if the lock is out of date.
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-dev

# Now the code (changes often -> last).
COPY app ./app

# Use the venv uv created without "activate".
ENV PATH="/app/.venv/bin:$PATH"

# Don't run as root: limits damage if the app is compromised.
RUN useradd --create-home appuser
USER appuser

# Documentation only; the real mapping is `-p host:8000` or the K8s Service.
EXPOSE 8000

# Bind 0.0.0.0, not 127.0.0.1, or nothing outside the container can reach it.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
