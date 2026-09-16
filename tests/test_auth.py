"""Security tests. EcoCI must never skip these."""

import pytest

from shop.auth import hash_password, issue_token, verify_password, verify_token

pytestmark = pytest.mark.security


def test_hash_password_roundtrip():
    stored = hash_password("correct horse battery")
    assert verify_password("correct horse battery", stored)


def test_hash_password_rejects_short():
    with pytest.raises(ValueError):
        hash_password("short")


def test_verify_password_rejects_wrong():
    stored = hash_password("correct horse battery")
    assert not verify_password("wrong password", stored)


def test_verify_password_rejects_malformed():
    assert not verify_password("anything", "not-a-hash")


def test_token_roundtrip():
    token = issue_token("user-1", "s3cret", now=1000)
    assert verify_token(token, "s3cret", now=1010) == "user-1"


def test_token_rejects_tampering():
    token = issue_token("user-1", "s3cret", now=1000)
    tampered = token.replace("user-1", "user-2")
    assert verify_token(tampered, "s3cret", now=1010) is None


def test_token_expires():
    token = issue_token("user-1", "s3cret", now=1000)
    assert verify_token(token, "s3cret", now=100000) is None


def test_token_rejects_wrong_secret():
    token = issue_token("user-1", "s3cret", now=1000)
    assert verify_token(token, "other", now=1010) is None
