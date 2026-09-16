"""Security: password hashing and token handling.

Tests for this module are tagged ``security`` and are never skipped by EcoCI,
regardless of what the classifier predicts.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import time

ITERATIONS = 120_000
TOKEN_TTL_S = 900


def hash_password(password: str, salt: str | None = None) -> str:
    if len(password) < 8:
        raise ValueError("password must be at least 8 characters")
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), ITERATIONS)
    return f"pbkdf2_sha256${ITERATIONS}${salt}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algorithm, iterations, salt, digest = stored.split("$")
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    candidate = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), int(iterations)
    ).hex()
    return hmac.compare_digest(candidate, digest)


def issue_token(user_id: str, secret: str, now: float | None = None) -> str:
    issued = int(now or time.time())
    payload = f"{user_id}:{issued}"
    signature = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{signature}"


def verify_token(token: str, secret: str, now: float | None = None) -> str | None:
    parts = token.split(":")
    if len(parts) != 3:
        return None
    user_id, issued, signature = parts
    payload = f"{user_id}:{issued}"
    expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        return None
    if int(now or time.time()) - int(issued) > TOKEN_TTL_S:
        return None
    return user_id
