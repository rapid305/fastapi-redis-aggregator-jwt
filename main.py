import logging
import time
from typing import Callable

from fastapi import FastAPI, Request
from api.routers.weatherRouter import router as weatherRouter
from api.routers.cryptoRouter import router as cryptoRouter
from api.auth.authRouter import router as authRouter

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API Agregator")


@app.middleware("http")
async def unified_middleware(request: Request, call_next: Callable):
    # Логирование заголовков
    logger.info(f"Incoming request headers: {request.headers}")

    # Замер времени выполнения
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"The response time is {process_time:.4f} seconds")

    return response


app.include_router(weatherRouter)
app.include_router(cryptoRouter)
app.include_router(authRouter)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
