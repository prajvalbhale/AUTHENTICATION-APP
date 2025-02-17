from fastapi import FastAPI, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
import requests
from jose import jwt

from src.utilite.jwt_helper import fetch_logged_in_user
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = 'http://127.0.0.1:8000'

router = APIRouter(
    prefix="/google-auth",
    tags=['Google Auth Controller']
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

@router.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }

@router.get("/auth/google")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    return user_info.json()

@router.get("/token")
async def get_token(token: str = Depends(fetch_logged_in_user)):
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])