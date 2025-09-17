import httpx
import os
from dotenv import load_dotenv
from typing import Dict, Optional
from fastapi import HTTPException

load_dotenv(override=True)


class CryptoCurrencyService:
    """
        Класс для обращения к внешнему API (coinmarketcap).
    """

    def __init__(
        self,
        api_key: str | None = os.getenv("COINMARKETCAP_API_KEY"),
        timeout: float = 5.0,
    ):
        self.base_url = "https://pro-api.coinmarketcap.com/v1"
        self.api_key = api_key
        if not self.api_key:
            raise RuntimeError("COINMARKETCAP_API_KEY is not set")
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

        self.headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": self.api_key,
        }

    async def get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout, headers=self.headers)
        return self._client

    async def get_cryptocurrencies(
        self, crypto: str, convert: str = "USD"
    ) -> Dict[str, any]:
        params = {"symbol": crypto, "convert": convert}
        url = f"{self.base_url}/cryptocurrency/quotes/latest"

        client = await self.get_client()
        try:
            resp = await client.get(url, params=params)
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, detail=f"Error connecting to CoinMarketCap: {e}"
            )

        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"CoinMarketCap API error: {resp.text}",
            )

        data = resp.json()
        return data


crypto_service = CryptoCurrencyService()
