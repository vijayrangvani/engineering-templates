"""TEMPLATE: JWT auth in FastAPI: register, login, protected route, role check (401 vs 403).

Run: uvicorn app.main:app --reload  -> /docs has an "Authorize" button (from OAuth2PasswordBearer).
Users live in a dict to keep the focus on auth; swap for the DB layer from fastapi-app/.
"""
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

from app.security import (
    DUMMY_HASH,
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)

app = FastAPI(title="auth-jwt")

# Tells FastAPI: read "Authorization: Bearer <token>"; tokenUrl = where /docs sends the login form.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

USERS: dict[str, dict] = {}   # username -> {"username", "hashed_password", "role"}


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)


class UserOut(BaseModel):
    username: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---- dependencies: reusable "who is calling?" checks ----
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},   # standard header for 401 with bearer auth
    )
    try:
        username = decode_token(token)
    except jwt.InvalidTokenError:
        raise unauthorized from None
    user = USERS.get(username)
    if not user:                      # token valid but user deleted
        raise unauthorized
    return user


CurrentUser = Annotated[dict, Depends(get_current_user)]


def require_admin(user: CurrentUser) -> dict:
    if user["role"] != "admin":
        # 403 = we know who you are, you're not allowed. (401 = we don't know who you are.)
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admins only")
    return user


# ---- routes ----
@app.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate):
    if data.username in USERS:
        raise HTTPException(status.HTTP_409_CONFLICT, "Username taken")
    role = "admin" if not USERS else "user"   # demo: first user becomes admin
    USERS[data.username] = {
        "username": data.username,
        "hashed_password": hash_password(data.password),
        "role": role,
    }
    return USERS[data.username]


@app.post("/token", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """OAuth2 standard: form fields `username` + `password` (not JSON)."""
    user = USERS.get(form.username)
    # Don't reveal which usernames exist: same error for "no user" and "wrong password", AND the
    # same timing. Argon2 is deliberately slow (~tens of ms), so skipping it for unknown users would
    # make them answer measurably faster. Always run one verify, against a dummy hash if needed.
    hashed = user["hashed_password"] if user else DUMMY_HASH
    password_ok = verify_password(form.password, hashed)
    if not user or not password_ok:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(user["username"]))


@app.get("/me", response_model=UserOut)
def me(user: CurrentUser):
    return user


@app.get("/admin/stats")
def admin_stats(user: Annotated[dict, Depends(require_admin)]):
    return {"users": len(USERS)}
