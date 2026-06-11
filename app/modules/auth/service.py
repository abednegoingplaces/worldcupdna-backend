"""Authentication logic: registration, login, token refresh, password reset."""
import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.modules.auth.schemas import (
    LoginRequest,
    PasswordResetConfirm,
    RegisterRequest,
)
from app.modules.users.models import User


def _tokens_for(user: User) -> tuple[str, str]:
    return (
        create_access_token({"sub": user.id}),
        create_refresh_token({"sub": user.id}),
    )


def register(db: Session, payload: RegisterRequest) -> tuple[User, str, str]:
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        favorite_team=payload.favorite_team,
        tactical_style=payload.tactical_style,
        rivalry_level=payload.rivalry_level if payload.rivalry_level is not None else 5,
        verification_token=str(uuid.uuid4()),
        is_verified=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access, refresh = _tokens_for(user)
    return user, access, refresh


def login(db: Session, payload: LoginRequest) -> tuple[User, str, str]:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")

    access, refresh = _tokens_for(user)
    return user, access, refresh


def refresh_access_token(db: Session, refresh_token: str) -> str:
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return create_access_token({"sub": user.id})


def verify_email(db: Session, token: str) -> None:
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    user.is_verified = True
    user.verification_token = None
    db.commit()


def request_password_reset(db: Session, email: str) -> None:
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.reset_token = str(uuid.uuid4())
        db.commit()
        # TODO: send reset email via SendGrid when SENDGRID_API_KEY is configured


def confirm_password_reset(db: Session, payload: PasswordResetConfirm) -> None:
    user = db.query(User).filter(User.reset_token == payload.token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    user.hashed_password = hash_password(payload.new_password)
    user.reset_token = None
    db.commit()
