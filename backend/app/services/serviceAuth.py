from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import DUMMY_PASSWORD_HASH, hash_password, verify_password
from app.models.user import User
from app.schemas.schemaUser import UserSignup


class EmailAlreadyRegistered(Exception):
    pass


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.scalar(select(User).where(User.email == email))


def register_user(session: Session, signup: UserSignup) -> User:
    if get_user_by_email(session, signup.email) is not None:
        raise EmailAlreadyRegistered

    user = User(
        full_name=signup.full_name,
        email=signup.email,
        hashed_password=hash_password(signup.password.get_secret_value()),
    )
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        # The unique constraint also protects against simultaneous signups.
        if get_user_by_email(session, signup.email) is not None:
            raise EmailAlreadyRegistered from None
        raise
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session, email)
    hashed_password = user.hashed_password if user is not None else DUMMY_PASSWORD_HASH
    valid_password = verify_password(password, hashed_password)
    return user if valid_password else None
