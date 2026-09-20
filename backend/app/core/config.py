import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field, SecretStr, ValidationError, field_validator

BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")

DATABASE_URL = os.getenv(
    "DATABASE_URL", f"sqlite:///{(BACKEND_DIR / 'kudagiri.db').as_posix()}"
)

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")
    if origin.strip()
]


class AuthSettings(BaseModel):
    secret_key: SecretStr
    access_token_expire_minutes: int = Field(default=30, ge=1, le=1440)

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, value: SecretStr) -> SecretStr:
        if len(value.get_secret_value().strip()) < 32:
            raise ValueError("SECRET_KEY must contain at least 32 characters")
        return value


def load_auth_settings() -> AuthSettings:
    try:
        return AuthSettings(
            secret_key=os.getenv("SECRET_KEY", ""),
            access_token_expire_minutes=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"),
        )
    except ValidationError:
        raise RuntimeError(
            "Set SECRET_KEY to a random value of at least 32 characters and "
            "ACCESS_TOKEN_EXPIRE_MINUTES to an integer from 1 to 1440 in backend/.env."
        ) from None
