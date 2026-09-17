from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from threading import Barrier

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import load_auth_settings
from app.core.security import AUDIENCE, ISSUER, verify_password
from app.database.sessions import create_database_engine
from app.main import create_app
from app.models.user import User
from app.services import serviceAuth

SIGNUP = {"full_name": "Test Guest", "email": "guest@example.com", "password": "Lake breeze 123"}
LOGIN = {"email": SIGNUP["email"], "password": SIGNUP["password"]}


@pytest.fixture
def registered_user(empty_client):
    response = empty_client.post("/api/auth/signup", json=SIGNUP)
    assert response.status_code == 201
    return response.json()


def test_signup_stores_hash_and_returns_only_public_fields(empty_client, engine):
    response = empty_client.post("/api/auth/signup", json={
        **SIGNUP, "email": " Guest@EXAMPLE.COM ", "full_name": "  Test Guest  ",
    })
    assert response.status_code == 201
    assert response.json() == {"id": 1, "email": "guest@example.com", "full_name": "Test Guest"}
    assert response.headers["cache-control"] == "no-store"
    with Session(engine) as session:
        user = session.get(User, 1)
        assert user.hashed_password.startswith("$argon2id$")
        assert user.hashed_password != SIGNUP["password"]
        assert verify_password(SIGNUP["password"], user.hashed_password)
        assert user.hashed_password not in response.text


def test_duplicate_email_is_case_insensitive(empty_client, registered_user, engine):
    response = empty_client.post("/api/auth/signup", json={**SIGNUP, "email": "GUEST@example.com"})
    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(User)) == 1


def test_concurrent_signups_return_conflict(empty_client, engine, monkeypatch):
    barrier = Barrier(2)
    original_lookup = serviceAuth.get_user_by_email

    def simultaneous_lookup(session, email):
        user = original_lookup(session, email)
        if user is None:
            barrier.wait(timeout=10)
        return user

    monkeypatch.setattr(serviceAuth, "get_user_by_email", simultaneous_lookup)
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(
            lambda _: empty_client.post("/api/auth/signup", json=SIGNUP), range(2),
        ))
    assert sorted(response.status_code for response in responses) == [201, 409]
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(User)) == 1


def test_login_and_authenticated_profile(empty_client, registered_user):
    response = empty_client.post("/api/auth/login", json={**LOGIN, "email": "GUEST@EXAMPLE.COM"})
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    token = response.json()
    assert token["token_type"] == "bearer"
    assert token["expires_in"] == 1800
    profile = empty_client.get("/api/auth/me", headers={"Authorization": f"Bearer {token['access_token']}"})
    assert profile.status_code == 200
    assert profile.json() == registered_user
    assert profile.headers["cache-control"] == "no-store"
    assert "password" not in profile.text


def test_wrong_password_and_unknown_email_have_same_error(empty_client, registered_user):
    responses = [
        empty_client.post("/api/auth/login", json={**LOGIN, "password": "wrong-password"}),
        empty_client.post("/api/auth/login", json={**LOGIN, "email": "unknown@example.com"}),
    ]
    for response in responses:
        assert response.status_code == 401
        assert response.headers["www-authenticate"] == "Bearer"
        assert response.json() == {"detail": "Incorrect email or password"}


@pytest.mark.parametrize("changes", [
    {"email": "not-an-email"}, {"full_name": " "}, {"full_name": "a" * 101},
    {"password": "short"}, {"password": "x" * 129}, {"password": " " * 8},
    {"password": 123456789}, {"role": "admin"}, {"email": None},
])
def test_invalid_signup_does_not_create_account(empty_client, engine, changes):
    response = empty_client.post("/api/auth/signup", json={**SIGNUP, **changes})
    assert response.status_code == 422
    assert all("input" not in error and "ctx" not in error for error in response.json()["detail"])
    assert SIGNUP["password"] not in response.text
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(User)) == 0


def test_password_not_echoed_in_validation_errors(empty_client):
    secret = "a-private-password-that-must-not-be-echoed"
    response = empty_client.post("/api/auth/signup", json={
        **SIGNUP, "password": {"unexpected": secret},
    })
    assert response.status_code == 422
    assert secret not in response.text
    response = empty_client.post("/api/auth/login", json={"email": "bad", "password": secret})
    assert response.status_code == 422
    assert secret not in response.text


def test_long_unicode_password_is_not_trimmed_or_truncated(empty_client):
    password = " " + "🌊" * 30 + "ending "
    assert empty_client.post("/api/auth/signup", json={**SIGNUP, "password": password}).status_code == 201
    assert empty_client.post("/api/auth/login", json={**LOGIN, "password": password}).status_code == 200
    for wrong_password in [password.strip(), " " + "🌊" * 30 + "different "]:
        assert empty_client.post("/api/auth/login", json={**LOGIN, "password": wrong_password}).status_code == 401


@pytest.mark.parametrize("authorization", [None, "Basic abc123", "Bearer", "Bearer garbage"])
def test_missing_or_malformed_bearer_token(empty_client, authorization):
    headers = {"Authorization": authorization} if authorization else {}
    response = empty_client.get("/api/auth/me", headers=headers)
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.parametrize(("changes", "missing"), [
    ({"exp": 1}, None), ({}, "exp"), ({}, "iat"), ({}, "sub"), ({}, "iss"), ({}, "aud"),
    ({"iss": "different-app"}, None), ({"aud": "different-client"}, None),
    ({"sub": "0"}, None), ({"sub": "-1"}, None), ({"sub": "abc"}, None),
    ({"sub": "9" * 50}, None), ({"sub": "9223372036854775808"}, None),
    ({"sub": "999"}, None), ({"sub": 1}, None), ({"token_type": "refresh"}, None),
    ({"iat": 9999999999}, None), ({"exp": None}, None), ({"exp": []}, None),
])
def test_invalid_token_claims(empty_client, registered_user, auth_settings, changes, missing):
    now = datetime.now(timezone.utc)
    claims = {
        "sub": str(registered_user["id"]), "iat": now, "exp": now + timedelta(minutes=30),
        "iss": ISSUER, "aud": AUDIENCE, "token_type": "access", **changes,
    }
    if missing:
        del claims[missing]
    token = jwt.encode(claims, auth_settings.secret_key.get_secret_value(), algorithm="HS256")
    response = empty_client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.parametrize("mode", ["wrong-key", "wrong-algorithm", "unsigned"])
def test_untrusted_token_signatures(empty_client, registered_user, auth_settings, mode):
    now = datetime.now(timezone.utc)
    claims = {
        "sub": str(registered_user["id"]), "iat": now, "exp": now + timedelta(minutes=30),
        "iss": ISSUER, "aud": AUDIENCE, "token_type": "access",
    }
    key = auth_settings.secret_key.get_secret_value()
    algorithm = "HS256"
    if mode == "wrong-key":
        key = "another-test-only-signing-key-" * 3
    elif mode == "wrong-algorithm":
        algorithm = "HS384"
    else:
        key, algorithm = "", "none"
    token = jwt.encode(claims, key, algorithm=algorithm)
    assert empty_client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_account_and_token_survive_app_restart(empty_client, registered_user, engine, auth_settings):
    token = empty_client.post("/api/auth/login", json=LOGIN).json()["access_token"]
    restarted_engine = create_database_engine(str(engine.url))
    try:
        with TestClient(create_app(restarted_engine, auth_settings)) as restarted:
            assert restarted.post("/api/auth/login", json=LOGIN).status_code == 200
            assert restarted.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).json() == registered_user
    finally:
        restarted_engine.dispose()


def test_deleted_user_cannot_use_old_token(empty_client, registered_user, engine):
    token = empty_client.post("/api/auth/login", json=LOGIN).json()["access_token"]
    with Session(engine) as session:
        session.delete(session.get(User, registered_user["id"]))
        session.commit()
    assert empty_client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401
    replacement = empty_client.post("/api/auth/signup", json={**SIGNUP, "email": "new@example.com"})
    assert replacement.status_code == 201
    assert replacement.json()["id"] != registered_user["id"]
    assert empty_client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_auth_cors_preflight(empty_client):
    response = empty_client.options("/api/auth/login", headers={
        "Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type,authorization",
    })
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "POST" in response.headers["access-control-allow-methods"]


@pytest.mark.parametrize("secret", ["", "short", " " * 40])
def test_startup_rejects_missing_or_weak_key(engine, monkeypatch, secret):
    monkeypatch.setenv("SECRET_KEY", secret)
    with pytest.raises(RuntimeError, match="Set SECRET_KEY"):
        with TestClient(create_app(engine)):
            pass


@pytest.mark.parametrize("minutes", ["0", "-1", "1441", "invalid"])
def test_invalid_token_lifetime(monkeypatch, auth_settings, minutes):
    monkeypatch.setenv("SECRET_KEY", auth_settings.secret_key.get_secret_value())
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", minutes)
    with pytest.raises(RuntimeError, match="ACCESS_TOKEN_EXPIRE_MINUTES"):
        load_auth_settings()
