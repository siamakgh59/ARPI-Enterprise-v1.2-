from fastapi import APIRouter
from app.market import market_live

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def dashboard_summary():

    data = market_live()

    analysis = data.get("analysis", {})

    signals = []

    
            "
