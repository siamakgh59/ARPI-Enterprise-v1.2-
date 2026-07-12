from fastapi import APIRouter

from .data.yahoo import get_market_snapshot


router = APIRouter(
    prefix="/market",
    tags=["Market"]
)


@router.get("")
def market_home():

    return {
        "module": "Market",
        "status": "online",
        "version": "1.3.0",
        "message": "ARPI Live Market Engine"
    }


@router.get("/live")
def market_live():

    data = get_market_snapshot()

    return {
        "module": "Market",
        "status": "success",
        "version": "1.3.0",
        "data": data
    }
