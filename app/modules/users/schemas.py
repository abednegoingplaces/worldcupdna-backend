from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserPublic(BaseModel):
    """A user as seen by other fans."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    favorite_team: Optional[str] = None
    tactical_style: Optional[str] = None
    avatar_url: Optional[str] = None
    total_points: int = 0


class UserMe(UserPublic):
    """The authenticated user's own profile."""
    email: str
    full_name: Optional[str] = None
    rivalry_level: Optional[int] = None
    is_verified: bool = False
    is_admin: bool = False


class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    favorite_team: Optional[str] = None
    tactical_style: Optional[str] = None
    rivalry_level: Optional[int] = None
    avatar_url: Optional[str] = None


class InterestsUpdate(BaseModel):
    favorite_team: Optional[str] = None
    tactical_style: Optional[str] = None
    rivalry_level: Optional[int] = None
