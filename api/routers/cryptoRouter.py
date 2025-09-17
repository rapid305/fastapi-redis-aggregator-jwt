from fastapi import APIRouter
from api.services.coinmarketcap import CryptoCurrencyService

router = APIRouter(prefix="/crypto", tags=["crypto"])

crypto_service = CryptoCurrencyService()


@router.get("/")
async def get_crypto(currency: str):
    return await crypto_service.get_cryptocurrencies(currency)
