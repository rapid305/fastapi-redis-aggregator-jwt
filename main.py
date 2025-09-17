import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from api.routers.weatherRouter import router as weatherRouter
from api.routers.cryptoRouter import router as cryptoRouter
from api.auth.authRouter import router as authRouter
import time
from typing import Callable
import logging

app = FastAPI()

app.include_router(weatherRouter)
app.include_router(cryptoRouter)

app.include_router(authRouter)

logging.basicConfig(level=logging.INFO)


@app.middleware("http")
async def middleware_timer(request: Request, call_next: Callable):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f"The response time is {process_time} seconds")
    return response


@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as e:
        return JSONResponse(
            status_code=500, content={"detail": "Internal Server Error"}
        )


if __name__ == "__main__":
    print("PyCharm")
