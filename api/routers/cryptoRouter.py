from fastapi import APIRouter, Depends

from api.services.coinmarketcap import CryptoCurrencyService
from api.auth.auth_service import get_current_active_user  # защита через JWT
from api.auth.auth_model import User

router = APIRouter(
    prefix="/crypto",
    tags=["crypto"],
)

crypto_service = CryptoCurrencyService()


@router.get("/")
async def get_crypto(
    currency: str,
    convert: str = "USD",
    current_user: User = Depends(get_current_active_user),
):
    return await crypto_service.get_cryptocurrencies(crypto=currency, convert=convert)
