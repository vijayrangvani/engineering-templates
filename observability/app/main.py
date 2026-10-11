"""TEMPLATE: the 3 things every production API needs to be debuggable.
1. Structured (JSON) logs  -> Loki/ELK can filter by field (status=500, path=/items)
2. Request ID on every log line + response header -> trace one request across services
3. Prometheus /metrics: request count + latency histogram -> Grafana dashboards + alerts
"""
import json
import logging
import sys
import time
import uuid
from contextvars import ContextVar

from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

# ---- 1 + 2: JSON logs carrying the current request id ----
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")  # per-request, async-safe


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "request_id": request_id_var.get(),
        }
        entry.update(getattr(record, "extra_fields", {}))   # fields passed via extra=
        return json.dumps(entry)


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)
log = logging.getLogger("api")

# ---- 3: metrics ----
REQUESTS = Counter("http_requests_total", "Requests", ["method", "path", "status"])
LATENCY = Histogram("http_request_duration_seconds", "Latency", ["method", "path"])

app = FastAPI(title="observability")


@app.middleware("http")
async def observe(request: Request, call_next):
    rid = request.headers.get("X-Request-ID") or uuid.uuid4().hex   # reuse caller's id if given
    request_id_var.set(rid)
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    # Label with the route TEMPLATE (/items/{id}), not the raw URL (/items/123): raw URLs create
    # a new time series per id and can crash Prometheus ("label cardinality explosion").
    route = request.scope.get("route")
    path = route.path if route else "unmatched"
    if path != "/metrics":
        REQUESTS.labels(request.method, path, response.status_code).inc()
        LATENCY.labels(request.method, path).observe(duration)
        log.info("request", extra={"extra_fields": {
            "method": request.method, "path": path,
            "status": response.status_code, "ms": round(duration * 1000, 1),
        }})
    response.headers["X-Request-ID"] = rid
    return response


@app.get("/items/{item_id}")
def get_item(item_id: int):
    log.info("fetching item", extra={"extra_fields": {"item_id": item_id}})
    return {"id": item_id}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)   # Prometheus text format
