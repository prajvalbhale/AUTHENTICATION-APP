from sqlalchemy.orm import Session
from src.models.user import User

class UserRepository:
    @staticmethod
    def create_user(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.userName == username).first()

    @staticmethod
    def get_users_created_by(db: Session, user_id: int):
        return db.query(User).filter(User.created_by == user_id).all()
