from fastapi import APIRouter

from .data.providers import get_best_market_data
from .intelligence.fusion import fusion_market


market_router = APIRouter(
    prefix="/market",
    tags=["Market"]
)


@market_router.get("")
def market_home():
    return {
        "module": "Market",
        "status": "online",
        "version": "1.4.0",
        "message": "ARPI Fusion Market Engine"
    }


@market_router.get("/live")
def market_live():

    raw_data = get_best_market_data()

    analysis = fusion_market(
        raw_data
    )

    return {
        "module": "Market",
        "status": "success",
        "version": "1.4.0",
        "raw_data": raw_data,
        "analysis": analysis
    }
