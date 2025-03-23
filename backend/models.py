from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    slack_user_id = Column(String, unique=True, nullable=True)
    slack_channel_id = Column(String, nullable=True)

class CFP(Base):
    __tablename__ = "cfps"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    event_name = Column(String)
    event_date = Column(DateTime)
    closing_date = Column(DateTime)
    location = Column(String)
    target_audience = Column(String)
    event_type = Column(String)
    event_url = Column(String)
    cfp_url = Column(String)
    source = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    created_by = relationship("User", back_populates="cfps")

User.cfps = relationship("CFP", back_populates="created_by") 