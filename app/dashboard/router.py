from fastapi import APIRouter
from datetime import datetime

from app.market import market_live

print("######## ARPI BOARD DASHBOARD v1.5 LOADED ########")


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def dashboard_summary():

    data = market_live()

    analysis = data.get("analysis", {})

    signals = []

    confidence_values = []

    risk_levels = []

    for asset, item in analysis.items():

        confidence = item.get("confidence", 0)

        signals.append({
            "asset": asset,
            "signal": item.get("signal"),
            "confidence": confidence,
            "risk": item.get("risk")
        })

        confidence_values.append(confidence)

        if item.get("risk"):
            risk_levels.append(item.get("risk"))


    avg_confidence = (
        sum(confidence_values) / len(confidence_values)
        if confidence_values
        else 0
    )


    risk_summary = {
        "HIGH": risk_levels.count("HIGH"),
        "MEDIUM": risk_levels.count("MEDIUM"),
        "LOW": risk_levels.count("LOW")
    }


    return {

        "application": "ARPI Enterprise",

        "version": "1.4.0",

        "timestamp": datetime.utcnow().isoformat(),


        "dashboard_status": "ACTIVE",


        "arpi_score": {
            "value": round(avg_confidence),
            "status": "calculating"
        },


        "market": {
            "status": "LIVE",
            "engine": "ARPI Market Engine"
        },


        "risk_summary": risk_summary,


        "assets": {
            "total": len(signals),
            "analyzed": signals
        },


        "decision_summary": {

            "top_signals": signals[:5],

            "overall_confidence": round(avg_confidence),

            "recommendation": "HOLD"

        }

    }
