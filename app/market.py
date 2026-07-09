from fastapi import APIRouter

market_router = APIRouter(prefix="/market", tags=["Market"])


@market_router.get("")
async def market_home():
    return {
        "module": "Market",
        "status": "online",
        "version": "1.2.0"
    }


@market_router.get("/live")
async def market_live():
    return {
        "status": "success",
        "data": {
            "gold": "coming soon",
            "usd": "coming soon",
            "oil": "coming soon",
            "vix": "coming soon"
        }
    }
