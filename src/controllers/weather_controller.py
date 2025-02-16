from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

from src.services.weather_service import CoinsService
from src.utilite.jwt_helper import fetch_logged_in_user

router = APIRouter(
    prefix="/weather",
    tags=["weather"]
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

@router.get("/temperature")
async def get_temperature(
        logged_in_user: dict = Depends(fetch_logged_in_user)
):
    return CoinsService.get_air_temperature()
