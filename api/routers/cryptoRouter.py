from fastapi import APIRouter, Depends

from api.services.coinmarketcap import CryptoCurrencyService
from api.auth.auth_service import (
    get_current_active_user,
)  # to protect the endpoint with auth (JWT)
from api.auth.auth_model import User
from api.services.coinmarketcap import crypto_service

router = APIRouter(
    prefix="/crypto",
    tags=["crypto"],
)


# Endpoint to get cryptocurrency data
@router.get("/")
async def get_crypto(
    currency: str,
    convert: str = "USD",
    current_user: User = Depends(get_current_active_user),
):
    return await crypto_service.get_cryptocurrencies(crypto=currency, convert=convert)
