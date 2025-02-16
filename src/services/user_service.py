from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from sqlalchemy.orm import Session
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.dtos.user_dto import CreateUserDTO
from fastapi import HTTPException, status

ALGORITHM = 'HS256'
SECRET_KEY = '404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970'
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserService:
    @staticmethod
    def create_user(db: Session, user_dto: CreateUserDTO, created_by: int):
        hashed_password = bcrypt_context.hash(user_dto.password)
        new_user = User(
            userName=user_dto.userName,
            password=hashed_password,
            userMail=user_dto.userMail,
            phone=user_dto.phone,
            address=user_dto.address,
            role=user_dto.role,
            created_by=created_by
        )
        return UserRepository.create_user(db, new_user)

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = UserRepository.get_user_by_username(db, username)
        if not user or not bcrypt_context.verify(password, user.password):
            return None
        return user

    @staticmethod
    def create_token(user: User, expires_delta: timedelta):
        encode = {
            'sub': user.userName,
            'id': user.id,
            'user': {
                'userName': user.userName,
                'userMail': user.userMail,
                'phone': user.phone,
                'created_by': user.created_by
            }
        }
        expires = datetime.utcnow() + expires_delta
        encode.update({'exp': expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get('sub')
            user_id = payload.get('id')
            if username is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            return {"username": username, "id": user_id}
        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
