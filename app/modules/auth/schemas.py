from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=2, max_length=40)
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: Optional[str] = None
    # Optional DNA profile captured during the profile builder flow
    favorite_team: Optional[str] = None
    tactical_style: Optional[str] = None
    rivalry_level: Optional[int] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class VerifyEmailRequest(BaseModel):
    token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=6)


class TokenUser(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    favorite_team: Optional[str] = None
    tactical_style: Optional[str] = None
    rivalry_level: Optional[int] = None
    total_points: int = 0
    is_verified: bool = False
    is_admin: bool = False


class AuthResponse(BaseModel):
    message: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: TokenUser
