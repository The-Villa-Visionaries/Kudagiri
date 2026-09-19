"""Local administrator command for granting or revoking ticket staff permission."""

import argparse

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import DATABASE_URL
from app.database.sessions import create_database_engine
from app.models.booking import TicketStaff
from app.models.user import User


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--email", required=True)
    parser.add_argument("--kind", choices=["ferry", "theme_park"], required=True)
    parser.add_argument("--revoke", action="store_true")
    args = parser.parse_args()
    engine = create_database_engine(DATABASE_URL)
    try:
        TicketStaff.__table__.create(engine, checkfirst=True)
        with Session(engine) as session:
            user = session.scalar(select(User).where(User.email == args.email.strip().lower()))
            if user is None:
                parser.error("Account not found; sign up before assigning permission.")
            permission = session.get(TicketStaff, (user.id, args.kind))
            if args.revoke:
                if permission is not None:
                    session.delete(permission)
            elif permission is None:
                session.add(TicketStaff(user_id=user.id, kind=args.kind))
            session.commit()
            print("Ticket staff permission revoked." if args.revoke else "Ticket staff permission granted.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
