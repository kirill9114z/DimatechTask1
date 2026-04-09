# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код до yield — выполняется при старте сервера
    print("Starting up...")
    yield
    # Код после yield — выполняется при остановке
    print("Shutting down...")


app = FastAPI(
    title="Payment API",
    description="REST API для работы с пользователями, счетами и платежами",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)


