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
