"""Promote a user to admin (or create one).

Run:  python -m scripts.create_admin <email>
If the user exists they are flagged is_admin/is_active/is_verified. Otherwise
you are prompted for a username and password to create the admin account.
"""
import sys
from getpass import getpass

from app.core.database import Base, SessionLocal, engine
from app import models_registry  # noqa: F401
from app.core.security import hash_password
from app.modules.users.models import User


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python -m scripts.create_admin <email>")
    email = sys.argv[1].strip().lower()

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.is_admin = True
            user.is_active = True
            user.is_verified = True
            db.commit()
            print(f"✅ {email} is now an admin")
            return

        username = input("Username for new admin: ").strip()
        password = getpass("Password: ")
        user = User(
            email=email,
            username=username,
            hashed_password=hash_password(password),
            is_admin=True,
            is_active=True,
            is_verified=True,
        )
        db.add(user)
        db.commit()
        print(f"✅ Created admin {username} <{email}>")
    finally:
        db.close()


if __name__ == "__main__":
    main()
