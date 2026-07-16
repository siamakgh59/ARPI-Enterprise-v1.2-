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

    for asset, item in analysis.items():
        signals.append({
            "asset": asset,
            "signal": item.get("signal"),
            "confidence": item.get("confidence"),
            "risk": item.get("risk")
        })


    return {
        "application": "ARPI Enterprise",
        "version": "1.4.0",

        "market_status": "ACTIVE",

        "top_signals": signals,

        "total_assets": len(signals)
    }
