# TEMPLATE: production Dockerfile for a Python API.
# Shape: base -> env -> workdir -> deps (cached layer) -> code -> non-root user -> port -> start command

# Slim official image: small, but has what pip needs. Pin the minor version.
FROM python:3.12-slim

# No .pyc files; logs go straight to stdout (so `docker logs` shows them immediately).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copy requirements FIRST: this layer is cached until requirements.txt changes,
# so code edits don't trigger a full reinstall.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Now the code (changes often -> last).
COPY app ./app

# Don't run as root: limits damage if the app is compromised.
RUN useradd --create-home appuser
USER appuser

# Documentation only; the real mapping is `-p host:8000` or the K8s Service.
EXPOSE 8000

# Bind 0.0.0.0, not 127.0.0.1, or nothing outside the container can reach it.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
