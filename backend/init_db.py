from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import SessionLocal
from models import User, CFP
from security import get_password_hash

def init_db():
    db = SessionLocal()
    try:
        # Create admin user
        admin_user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            slack_user_id="U123456789",
            slack_channel_id="C123456789"
        )
        db.add(admin_user)
        db.commit()

        # Create sample CFPs
        sample_cfps = [
            {
                "title": "Python Conference 2024",
                "description": "Annual Python conference focusing on the latest developments in Python programming.",
                "event_name": "PyCon 2024",
                "event_date": datetime.now() + timedelta(days=90),
                "closing_date": datetime.now() + timedelta(days=30),
                "location": "San Francisco, CA",
                "target_audience": "Python Developers",
                "event_type": "Conference",
                "event_url": "https://pycon.org/2024",
                "cfp_url": "https://pycon.org/2024/cfp",
                "source": "PyCon",
                "created_by_id": 1
            },
            {
                "title": "Web Development Summit",
                "description": "A comprehensive summit covering modern web development technologies and practices.",
                "event_name": "WebDev Summit 2024",
                "event_date": datetime.now() + timedelta(days=120),
                "closing_date": datetime.now() + timedelta(days=45),
                "location": "New York, NY",
                "target_audience": "Web Developers",
                "event_type": "Summit",
                "event_url": "https://webdevsummit.com/2024",
                "cfp_url": "https://webdevsummit.com/2024/cfp",
                "source": "WebDev Summit",
                "created_by_id": 1
            },
            {
                "title": "AI & Machine Learning Workshop",
                "description": "Hands-on workshop on implementing AI and ML solutions in production.",
                "event_name": "AI/ML Workshop 2024",
                "event_date": datetime.now() + timedelta(days=60),
                "closing_date": datetime.now() + timedelta(days=15),
                "location": "Remote",
                "target_audience": "AI/ML Engineers",
                "event_type": "Workshop",
                "event_url": "https://aimlworkshop.com/2024",
                "cfp_url": "https://aimlworkshop.com/2024/cfp",
                "source": "AI/ML Workshop",
                "created_by_id": 1
            }
        ]

        for cfp_data in sample_cfps:
            cfp = CFP(
                **cfp_data,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(cfp)
        
        db.commit()
        print("Database initialized successfully!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 