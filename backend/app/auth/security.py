"""
Password hashing (bcrypt, used directly — not via passlib, which is
unmaintained and incompatible with bcrypt>=4.1's API change) and JWT
creation/decoding (python-jose).
"""

from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt

from app.core.config import get_settings

settings = get_settings()

# bcrypt's underlying algorithm only uses the first 72 bytes of the input;
# anything beyond that is silently ignored. This is a known bcrypt
# limitation, not a bug introduced here — flagged so it isn't mistaken
# for one later.
_BCRYPT_MAX_PASSWORD_BYTES = 72


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password for storage. Never store plain_password directly."""
    password_bytes = plain_password.encode("utf-8")[:_BCRYPT_MAX_PASSWORD_BYTES]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plaintext password against a stored bcrypt hash."""
    password_bytes = plain_password.encode("utf-8")[:_BCRYPT_MAX_PASSWORD_BYTES]
    try:
        return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
    except ValueError:
        # Raised if hashed_password isn't a valid bcrypt hash (e.g. corrupted
        # data). Treat as "doesn't match" rather than letting it bubble up
        # as a 500 error.
        return False


def create_access_token(subject: str, extra_claims: dict[str, Any] | None = None) -> str:
    """
    Creates a signed JWT. `subject` is the user's id (stored in the
    standard `sub` claim). `extra_claims` can carry things like role,
    so route guards don't need a DB lookup just to check permissions.
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": expire,
    }
    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Decodes and verifies a JWT. Returns None if invalid/expired rather than raising,
    so callers can return a clean 401 instead of leaking a stack trace."""
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None
