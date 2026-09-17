from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import create_access_token, decode_access_token
from app.database.sessions import get_database
from app.models.user import User
from app.schemas.schemaUser import Token, UserLogin, UserRead, UserSignup
from app.services import serviceAuth

router = APIRouter(prefix="/auth", tags=["Authentication"])
Database = Annotated[Session, Depends(get_database)]
bearer_scheme = HTTPBearer(auto_error=False)
Credentials = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]


def unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(request: Request, database: Database, credentials: Credentials) -> User:
    if credentials is None:
        raise unauthorized("Invalid or expired authentication token")
    try:
        user_id = decode_access_token(credentials.credentials, request.app.state.auth_settings)
    except jwt.InvalidTokenError:
        raise unauthorized("Invalid or expired authentication token") from None
    user = database.get(User, user_id)
    if user is None:
        raise unauthorized("Invalid or expired authentication token")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    "/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Email already registered"}},
)
def signup(data: UserSignup, database: Database, response: Response):
    try:
        user = serviceAuth.register_user(database, data)
    except serviceAuth.EmailAlreadyRegistered:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered") from None
    response.headers["Cache-Control"] = "no-store"
    return user


@router.post(
    "/login", response_model=Token,
    responses={401: {"description": "Incorrect email or password"}},
)
def login(data: UserLogin, database: Database, request: Request, response: Response):
    user = serviceAuth.authenticate_user(database, data.email, data.password.get_secret_value())
    if user is None:
        raise unauthorized("Incorrect email or password")
    settings = request.app.state.auth_settings
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return Token(
        access_token=create_access_token(user.id, settings),
        expires_in=settings.access_token_expire_minutes * 60,
    )


@router.get("/me", response_model=UserRead, responses={401: {"description": "Invalid credentials"}})
def read_current_user(user: CurrentUser, response: Response):
    response.headers["Cache-Control"] = "no-store"
    return user
