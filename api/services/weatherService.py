import httpx
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from typing import Dict, Optional, Any
from api.db.redis import redis_client

load_dotenv(verbose=True)


# cryptocurrency service to interact with openWeather API
class WeatherClient:

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.openweathermap.org/data/2.5",
        timeout: float = 5.0,
    ):
        self.api_key = api_key or os.getenv("API_KEY")
        if not self.api_key:
            raise RuntimeError("Не указан OPENWEATHER_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def current_weather(
        self,
        city: str,
        units: str = "metric",
        lang: str = "ru",
    ) -> Dict[str, Any]:

        # Check cache first
        cache_key = f"weather:{city}:{units}:{lang}"
        cached_data = await redis_client.get_json(cache_key)
        if cached_data:
            return cached_data

        params = {
            "q": city,
            "appid": self.api_key,
            "units": units,
            "lang": lang,
        }
        url = f"{self.base_url}/weather"

        client = await self._get_client()
        try:
            resp = await client.get(url, params=params)
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Сеть недоступна: {e}") from e

        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Город не найден")
        if resp.status_code >= 400:
            raise HTTPException(
                status_code=502, detail=f"Ошибка внешнего сервиса: {resp.text}"
            )

        data = resp.json()

        # Data normalization
        normalized = {
            "city": data.get("name"),
            "temp": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "humidity": data.get("main", {}).get("humidity"),
            "weather": data.get("weather", [{}])[0].get("description"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "dt": data.get("dt"),
        }
        result = {"data": normalized}

        await redis_client.cache_json(cache_key, result, ttl=300)  # Cache for 5 minutes

        return result
