from sqlalchemy.orm import Session
from app import models
from app.core.security import get_password_hash
from app.db.session import SessionLocal

def init_db() -> None:
    db = SessionLocal()
    try:
        create_initial_admin(db)
    finally:
        db.close()

def create_initial_admin(db: Session) -> None:
    from app.core.config import settings  # Import settings here to avoid circular import
    admin_user = db.query(models.user_model.User).filter(models.user_model.User.username == settings.ADMIN_USERNAME).first()
    if not admin_user:
        admin_user = models.user_model.User(
            username=settings.ADMIN_USERNAME,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            is_admin=True,
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)