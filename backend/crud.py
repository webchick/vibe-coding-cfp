from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from . import models, schemas
from .config import settings

# User operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        slack_user_id=user.slack_user_id,
        slack_channel_id=user.slack_channel_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# CFP operations
def get_cfps(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    location: Optional[str] = None,
    target_audience: Optional[str] = None,
    event_type: Optional[str] = None,
    closing_date: Optional[datetime] = None
):
    query = db.query(models.CFP)
    
    if location:
        query = query.filter(models.CFP.location.ilike(f"%{location}%"))
    if target_audience:
        query = query.filter(models.CFP.target_audience.ilike(f"%{target_audience}%"))
    if event_type:
        query = query.filter(models.CFP.event_type.ilike(f"%{event_type}%"))
    if closing_date:
        query = query.filter(models.CFP.closing_date <= closing_date)
    
    return query.order_by(models.CFP.closing_date).offset(skip).limit(limit).all()

def create_cfp(db: Session, cfp: schemas.CFPCreate, user_id: int):
    db_cfp = models.CFP(
        **cfp.dict(),
        created_by_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_cfp)
    db.commit()
    db.refresh(db_cfp)
    return db_cfp

def get_cfp(db: Session, cfp_id: int):
    return db.query(models.CFP).filter(models.CFP.id == cfp_id).first()

# Slack notification operations
def send_slack_notification(db: Session, cfp_ids: List[int], channel_id: Optional[str] = None) -> schemas.NotificationResponse:
    client = WebClient(token=settings.SLACK_BOT_TOKEN)
    target_channel = channel_id or settings.SLACK_CHANNEL_ID
    
    if not target_channel:
        return schemas.NotificationResponse(
            success=False,
            message="No Slack channel specified",
            sent_to=""
        )
    
    cfps = [get_cfp(db, cfp_id) for cfp_id in cfp_ids]
    if not cfps:
        return schemas.NotificationResponse(
            success=False,
            message="No CFPs found",
            sent_to=target_channel
        )
    
    message = "🎯 New CFP Notifications:\n\n"
    for cfp in cfps:
        message += f"*{cfp.title}*\n"
        message += f"Event: {cfp.event_name}\n"
        message += f"Date: {cfp.event_date.strftime('%Y-%m-%d')}\n"
        message += f"Closing: {cfp.closing_date.strftime('%Y-%m-%d')}\n"
        message += f"Location: {cfp.location}\n"
        message += f"Target Audience: {cfp.target_audience}\n"
        message += f"Event URL: {cfp.event_url}\n"
        message += f"CFP URL: {cfp.cfp_url}\n\n"
    
    try:
        response = client.chat_postMessage(
            channel=target_channel,
            text=message,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                }
            ]
        )
        return schemas.NotificationResponse(
            success=True,
            message="Notifications sent successfully",
            sent_to=target_channel
        )
    except SlackApiError as e:
        return schemas.NotificationResponse(
            success=False,
            message=f"Error sending notification: {str(e)}",
            sent_to=target_channel
        ) 