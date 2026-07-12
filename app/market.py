from fastapi import APIRouter
from .data.providers import get_best_market_data

market_router = APIRouter(
    prefix="/market",
    tags=["Market"]
)


@market_router.get("")
def market_home():
    return {
        "module": "Market",
        "status": "online",
        "version": "1.3.0",
        "message": "ARPI Live Market Engine"
    }


@market_router.get("/live")
def market_live():
data = get_best_market_data()

    return {
        "module": "Market",
        "status": "success",
        "version": "1.3.0",
        "data": data
    }
