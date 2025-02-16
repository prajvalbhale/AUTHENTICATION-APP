from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from database import SessionLocal
from src.dtos.user_dto import CreateUserDTO, UpdateUserDTO
from src.services.user_service import UserService
from src.repositories.user_repository import UserRepository
from src.utilite.jwt_helper import fetch_logged_in_user
from src.models.user import User

router = APIRouter(
    prefix="/users",
    tags=['Users Controller']
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user_account(
        user_data: CreateUserDTO,
        db: Session = Depends(get_db),
        logged_in_user: dict = Depends(fetch_logged_in_user)):
    return UserService.create_user(db, user_data, created_by=logged_in_user['id'])


@router.get("/fetch-all-users", status_code=status.HTTP_200_OK)
async def get_users_created_by_logged_in_user(
        token: str = Depends(oauth2_bearer),
        db: Session = Depends(get_db)):
    user_data = UserService.verify_token(token)
    return UserRepository.get_users_created_by(db, user_data['id'])


@router.put("/user/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
        user_id: int,
        updated_data: UpdateUserDTO,
        db: Session = Depends(get_db),
        logged_in_user: dict = Depends(fetch_logged_in_user)):
    return UserRepository.update_user(db, user_id, updated_data.model_dump(exclude_unset=True), logged_in_user)
