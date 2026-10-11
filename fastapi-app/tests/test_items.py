"""TEMPLATE: API tests with a throwaway DB. Shape: fixture DB -> override dependency -> call -> assert."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

# In-memory SQLite; StaticPool keeps ONE connection so all sessions see the same DB.
engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def override_get_db():
    db = TestingSession()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@pytest.fixture
def client():
    Base.metadata.create_all(engine)
    app.dependency_overrides[get_db] = override_get_db   # swap real DB for test DB
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)                       # clean slate per test


def test_create_and_get(client):
    r = client.post("/items", json={"name": "pen", "price": 10})
    assert r.status_code == 201
    item_id = r.json()["id"]
    assert client.get(f"/items/{item_id}").json()["name"] == "pen"


def test_validation_error(client):
    assert client.post("/items", json={"name": "", "price": -1}).status_code == 422


def test_update_and_delete(client):
    item_id = client.post("/items", json={"name": "pen", "price": 10}).json()["id"]
    assert client.patch(f"/items/{item_id}", json={"price": 12}).json()["price"] == 12
    assert client.delete(f"/items/{item_id}").status_code == 204
    assert client.get(f"/items/{item_id}").status_code == 404


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}
