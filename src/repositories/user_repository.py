from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

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

    @staticmethod
    def update_user(db: Session, user_id: int, updated_data: dict, updated_by: dict):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        updated_data.pop("password", None)
        updated_data.pop("created_by", None)
        updated_data.pop("role", None)
        for key, value in updated_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user