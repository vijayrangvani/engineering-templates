import time

from fastapi.testclient import TestClient

from app.main import app


def test_job_runs_in_background():
    with TestClient(app) as client:          # `with` runs lifespan (creates tables)
        r = client.post("/reports", json={"topic": "sales"})
        assert r.status_code == 202 and r.json()["status"] == "pending"
        # TestClient finishes background tasks before returning, so the job is done here.
        done = client.get(f"/reports/{r.json()['id']}").json()
        assert done["status"] == "done" and "sales" in done["result"]


def test_gather_runs_concurrently():
    with TestClient(app) as client:
        start = time.perf_counter()
        assert client.get("/parallel").json()["results"] == ["a", "b", "c"]
        assert time.perf_counter() - start < 0.25    # 3 x 0.1s concurrently, not 0.3s in sequence
