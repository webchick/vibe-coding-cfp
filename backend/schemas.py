from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr
    slack_user_id: Optional[str] = None
    slack_channel_id: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class CFPBase(BaseModel):
    title: str
    description: str
    event_name: str
    event_date: datetime
    closing_date: datetime
    location: str
    target_audience: str
    event_type: str
    event_url: str
    cfp_url: str
    source: str

class CFPCreate(CFPBase):
    pass

class CFP(CFPBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class NotificationRequest(BaseModel):
    cfp_ids: List[int]
    channel_id: Optional[str] = None

class NotificationResponse(BaseModel):
    success: bool
    message: str
    sent_to: str 