import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_request_id_generated_and_echoed():
    assert len(client.get("/items/1").headers["X-Request-ID"]) == 32
    assert client.get("/items/1", headers={"X-Request-ID": "abc"}).headers["X-Request-ID"] == "abc"


def test_metrics_use_route_template_not_raw_url():
    client.get("/items/42")
    body = client.get("/metrics").text
    assert 'path="/items/{item_id}"' in body
    assert 'path="/items/42"' not in body
    assert "http_request_duration_seconds_bucket" in body


def test_crash_is_counted_as_500():
    # raise_server_exceptions=False: get the 500 response instead of the error re-raised in the test
    crash_client = TestClient(app, raise_server_exceptions=False)
    assert crash_client.get("/fail").status_code == 500
    assert 'path="/fail",status="500"' in client.get("/metrics").text


def test_crash_is_not_swallowed():
    with pytest.raises(RuntimeError, match="boom"):   # the middleware re-raised it, didn't hide it
        client.get("/fail")
