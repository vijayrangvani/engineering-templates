"""TEMPLATE: password hashing + JWT create/verify. No FastAPI here: pure functions, easy to test.

Flow:  register -> hash_password -> store hash (NEVER the password)
       login    -> verify_password -> create_access_token -> client stores token
       request  -> "Authorization: Bearer <token>" -> decode_token -> who is calling
"""
import logging
import os
from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

log = logging.getLogger(__name__)
DEV_SECRET = "dev-only-change-me-dev-only-change-me"


def load_secret(env: dict[str, str]) -> str:
    """Secret signs tokens: anyone with it can forge logins. Load from env, long and random:
        python -c "import secrets; print(secrets.token_hex(32))"
    Missing secret outside dev -> refuse to start. A public fallback would let anyone forge tokens.
    """
    secret = env.get("JWT_SECRET")
    if secret:
        return secret
    if env.get("ENVIRONMENT", "dev") != "dev":
        raise RuntimeError("JWT_SECRET must be set when ENVIRONMENT is not 'dev'")
    log.warning("JWT_SECRET not set: using the insecure dev secret")
    return DEV_SECRET


SECRET_KEY = load_secret(dict(os.environ))
ALGORITHM = "HS256"            # symmetric: same secret signs and verifies
ACCESS_TOKEN_MINUTES = 30      # short-lived; use refresh tokens for long sessions

password_hash = PasswordHash.recommended()   # Argon2 with sensible defaults (salted automatically)

# Hash of a throwaway password, used when the username doesn't exist (see login in main.py).
DUMMY_HASH = password_hash.hash("dummy-password-never-matches")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)   # constant-time compare inside


def create_access_token(subject: str, minutes: int = ACCESS_TOKEN_MINUTES) -> str:
    payload = {
        "sub": subject,                                          # who the token is for
        "exp": datetime.now(UTC) + timedelta(minutes=minutes),   # PyJWT rejects expired tokens
        "iat": datetime.now(UTC),                                # issued at
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> str:
    """Return the username. Raises jwt.InvalidTokenError (bad signature, expired, garbage)."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # ALWAYS pin algorithms
    return payload["sub"]
