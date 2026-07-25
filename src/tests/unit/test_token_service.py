from types import SimpleNamespace

import pytest

from auth.application.exceptions.user_exception import InvalidTokenError
from auth.infrastructure.services.token import TokenServiceJWT


def _service() -> TokenServiceJWT:
    settings = SimpleNamespace(
        token_secret_key="test-secret-key-that-is-long-enough-32b",
        jwt_config=SimpleNamespace(jwt_hashing="HS256"),
    )
    return TokenServiceJWT(settings)


def test_generate_and_decode_roundtrip():
    svc = _service()
    token = svc.generate_token({"id": "1", "token_type": "access"}, expires=15)
    payload = svc.decode_token(token)
    assert payload["id"] == "1"
    assert payload["token_type"] == "access"
    assert "exp" in payload


def test_tampered_token_raises():
    svc = _service()
    token = svc.generate_token({"id": "1"}, expires=15)
    with pytest.raises(InvalidTokenError):
        svc.decode_token(token + "tampered")


def test_expired_token_raises():
    svc = _service()
    token = svc.generate_token({"id": "1"}, expires=-1)
    with pytest.raises(InvalidTokenError):
        svc.decode_token(token)
