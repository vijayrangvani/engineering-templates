"""PRACTICE: app entry point.
Reference answer: ../../../fastapi-app/app/main.py

Shape:
  1. lifespan: create_all tables on startup -> yield -> engine.dispose()
  2. app = FastAPI(title=..., lifespan=lifespan)
  3. CORS middleware (explicit origins)
  4. include_router(items.router)
  5. GET /health -> {"status": "ok"}     GET /ready -> run SELECT 1, {"status": "ready"}
"""
# TODO
