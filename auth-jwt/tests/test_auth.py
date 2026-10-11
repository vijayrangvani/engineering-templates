import pytest
from fastapi.testclient import TestClient

from app.main import USERS, app
from app.security import create_access_token


@pytest.fixture
def client():
    USERS.clear()                     # isolate tests
    return TestClient(app)


def register_and_login(client, username, password="secret123"):
    client.post("/register", json={"username": username, "password": password})
    r = client.post("/token", data={"username": username, "password": password})  # form data
    return r.json()["access_token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_password_is_hashed(client):
    client.post("/register", json={"username": "alice", "password": "secret123"})
    assert USERS["alice"]["hashed_password"] != "secret123"


def test_login_and_me(client):
    token = register_and_login(client, "alice")
    r = client.get("/me", headers=auth(token))
    assert r.status_code == 200 and r.json()["username"] == "alice"


def test_wrong_password_401(client):
    register_and_login(client, "alice")
    r = client.post("/token", data={"username": "alice", "password": "wrongpass"})
    assert r.status_code == 401


def test_no_token_401(client):
    assert client.get("/me").status_code == 401


def test_expired_token_401(client):
    register_and_login(client, "alice")
    expired = create_access_token("alice", minutes=-1)
    assert client.get("/me", headers=auth(expired)).status_code == 401


def test_role_check_403(client):
    admin = register_and_login(client, "admin1")      # first user = admin
    user = register_and_login(client, "bob")
    assert client.get("/admin/stats", headers=auth(admin)).status_code == 200
    assert client.get("/admin/stats", headers=auth(user)).status_code == 403
