"""TEMPLATE: calling an external API safely: timeout + retries with backoff + clear errors.

Uses only httpx. Run: python http_client_retry.py
"""
import logging
import time

import httpx

log = logging.getLogger(__name__)
RETRY_STATUS = {429, 500, 502, 503, 504}       # temporary errors worth retrying


def get_json(url: str, retries: int = 3, timeout: float = 10.0) -> dict:
    for attempt in range(1, retries + 1):
        try:
            r = httpx.get(url, timeout=timeout)   # ALWAYS set a timeout
            if r.status_code in RETRY_STATUS:
                raise httpx.HTTPStatusError("retryable", request=r.request, response=r)
            r.raise_for_status()                  # 4xx -> error now, no retry (our request is wrong)
            return r.json()
        except (httpx.TransportError, httpx.HTTPStatusError) as e:
            retryable = isinstance(e, httpx.TransportError) or e.response.status_code in RETRY_STATUS
            if not retryable or attempt == retries:
                raise
            wait = 2 ** attempt                   # exponential backoff: 2s, 4s, 8s...
            log.warning("attempt %d failed (%s); retrying in %ss", attempt, e, wait)
            time.sleep(wait)
    raise RuntimeError("unreachable")


async def get_json_async(client: httpx.AsyncClient, url: str) -> dict:
    """Async version: share ONE AsyncClient for many calls (connection reuse)."""
    r = await client.get(url, timeout=10.0)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(get_json("https://httpbin.org/json")["slideshow"]["title"])
