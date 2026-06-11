from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth import service
from app.modules.auth.schemas import (
    AuthResponse,
    LoginRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RefreshRequest,
    RegisterRequest,
    VerifyEmailRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user, access, refresh = service.register(db, payload)
    return {
        "message": "Account created successfully!",
        "access_token": access,
        "refresh_token": refresh,
        "user": user,
    }


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user, access, refresh = service.login(db, payload)
    return {
        "message": "Login successful!",
        "access_token": access,
        "refresh_token": refresh,
        "user": user,
    }


@router.post("/refresh")
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    return {
        "access_token": service.refresh_access_token(db, payload.refresh_token),
        "token_type": "bearer",
    }


@router.post("/logout")
def logout():
    # Stateless JWT — the client discards the token. Endpoint kept for symmetry.
    return {"message": "Logged out successfully"}


@router.post("/verify-email")
def verify_email(payload: VerifyEmailRequest, db: Session = Depends(get_db)):
    service.verify_email(db, payload.token)
    return {"message": "Email verified successfully!"}


@router.post("/password-reset/request")
def password_reset_request(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    service.request_password_reset(db, payload.email)
    return {"message": "If that email exists, a reset link has been sent"}


@router.post("/password-reset/confirm")
def password_reset_confirm(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    service.confirm_password_reset(db, payload)
    return {"message": "Password reset successfully!"}


@router.get("/google")
def google_login():
    return {"message": "Google OAuth coming soon"}


@router.get("/google/callback")
def google_callback():
    return {"message": "Google OAuth callback coming soon"}
