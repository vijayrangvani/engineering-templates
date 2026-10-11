import os

# Must be set BEFORE app.db is imported (it reads the URL at import time).
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_async.db"


def pytest_sessionfinish(session, exitstatus):
    if os.path.exists("test_async.db"):
        os.remove("test_async.db")
