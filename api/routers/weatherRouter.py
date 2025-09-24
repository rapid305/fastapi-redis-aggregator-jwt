from fastapi import APIRouter
from api.services.weatherService import WeatherClient
from fastapi import Depends
from api.auth.auth_service import get_current_active_user
from api.auth.auth_model import User

router = APIRouter(prefix="/weather", tags=["weather"])

weatherClient = WeatherClient()


@router.get("/{city}")
async def get_weather(city: str, user: User = Depends(get_current_active_user)):
    return await weatherClient.current_weather(city)
