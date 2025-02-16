from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from src.dtos.user_dto import CreateUserDTO, TokenDTO
from database import SessionLocal
from src.services.user_service import UserService
from src.repositories.user_repository import UserRepository

router = APIRouter(
    prefix="/auth",
    tags=['Authentication Controller']
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/admin", status_code=status.HTTP_201_CREATED)
async def create_admin_account(
        user_data: CreateUserDTO,
        db: Session = Depends(get_db)
):
    return UserService.create_user(db, user_data, created_by=0)

@router.post("/token", response_model=TokenDTO)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = UserService.create_token(user, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
