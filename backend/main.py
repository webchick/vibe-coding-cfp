from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from .database import SessionLocal, engine
from . import models, schemas, crud
from .config import Settings
from .auth import get_current_user

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CFP Tracker API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to CFP Tracker API"}

@app.get("/cfps/", response_model=List[schemas.CFP])
async def get_cfps(
    skip: int = 0,
    limit: int = 100,
    location: Optional[str] = None,
    target_audience: Optional[str] = None,
    event_type: Optional[str] = None,
    closing_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get all CFPs with optional filtering"""
    return crud.get_cfps(
        db,
        skip=skip,
        limit=limit,
        location=location,
        target_audience=target_audience,
        event_type=event_type,
        closing_date=closing_date
    )

@app.post("/cfps/", response_model=schemas.CFP)
async def create_cfp(
    cfp: schemas.CFPCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new CFP"""
    return crud.create_cfp(db=db, cfp=cfp)

@app.post("/notify/", response_model=schemas.NotificationResponse)
async def send_slack_notification(
    cfp_ids: List[int],
    channel_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Send Slack notification for selected CFPs"""
    return crud.send_slack_notification(db=db, cfp_ids=cfp_ids, channel_id=channel_id)

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    """Get current user information"""
    return current_user 