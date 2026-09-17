from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError

from app.core.config import AuthSettings

ALGORITHM = "HS256"
ISSUER = "kudagiri-api"
AUDIENCE = "kudagiri-client"
password_hash = PasswordHash.recommended()
# Unknown accounts still perform a password check, like known accounts.
DUMMY_PASSWORD_HASH = password_hash.hash("not-a-real-account-password")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return password_hash.verify(password, hashed_password)
    except (UnknownHashError, ValueError):
        return False


def create_access_token(user_id: int, settings: AuthSettings) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
            "iss": ISSUER,
            "aud": AUDIENCE,
            "token_type": "access",
        },
        settings.secret_key.get_secret_value(),
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str, settings: AuthSettings) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[ALGORITHM],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={"require": ["sub", "iat", "exp", "iss", "aud"]},
        )
    except (TypeError, ValueError, OverflowError):
        # Malformed date claims can raise conversion errors in the JWT library.
        raise jwt.InvalidTokenError("Malformed token claims") from None
    subject = payload["sub"]
    # IDs must fit SQLite's signed 64-bit integer range.
    if not isinstance(subject, str) or not subject.isascii() or not subject.isdecimal():
        raise jwt.InvalidTokenError("Invalid subject")
    if len(subject) > 19 or not 0 < int(subject) <= 2**63 - 1:
        raise jwt.InvalidTokenError("Invalid subject")
    if payload.get("token_type") != "access":
        raise jwt.InvalidTokenError("Invalid token type")
    return int(subject)
