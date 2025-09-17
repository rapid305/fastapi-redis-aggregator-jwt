from fastapi import APIRouter
from api.services.weatherService import WeatherClient

router = APIRouter(prefix="/weather", tags=["weather"])

weatherClient = WeatherClient()


@router.get("/{city}")
async def get_weather(city: str):
    return await weatherClient.current_weather(city)
