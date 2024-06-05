from datetime import datetime
from typing import Optional

from data.database import BaseModel
from data.tables import UserStatus


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    organization_name: str
    is_internal: bool
    profile_image: Optional[str]
    status: UserStatus
    created_at: datetime
    updated_at: datetime
    internal_email: Optional[str]

    model_config = {"from_attributes": True}


class PartialUser(BaseModel):
    id: str
    name: str
    profile_image: str


class UserInfo(BaseModel):
    name: str
    given_name: str
    family_name: Optional[str] = None
    picture: Optional[str] = None
    email: str
    hd: Optional[str] = None

