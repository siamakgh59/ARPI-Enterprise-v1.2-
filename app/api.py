from fastapi import APIRouter

from app.market import market_router
from app.engines.macro.router import macro_router
from app.engines.gold.router import gold_router


api_router = APIRouter()


@api_router.get("/")
async def root():
    return {
        "application": "ARPI Enterprise",
        "version": "1.4.0",
        "status": "online"
    }


@api_router.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@api_router.get("/api-test")
async def api_test():
    return {
        "message": "API is working"
    }


# Market Engine
api_router.include_router(
    market_router
)


# Macro Intelligence Engine
api_router.include_router(
    macro_router
)


# Gold Intelligence Engine
api_router.include_router(
    gold_router
)
