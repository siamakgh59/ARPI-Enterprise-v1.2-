from fastapi import APIRouter
from datetime import datetime

from app.market import market_live
from app.engines.reasoning_engine import generate_reasoning

from app.engines.risk.engine import RiskEngine
from app.engines.risk.market_adapter import market_to_risk_factors


print("######## ARPI BOARD DASHBOARD v1.6 RIE CONNECTED ########")


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


risk_engine = RiskEngine()


@router.get("/summary")
def dashboard_summary():

    data = market_live()

    analysis = data.get(
        "analysis",
        {}
    )


    signals = []

    confidence_values = []

    risk_levels = []


    for asset, item in analysis.items():

        confidence = item.get(
            "confidence",
            0
        )

        signal = item.get(
            "signal"
        )


        factors = market_to_risk_factors(
            item
        )


        risk_report = risk_engine.analyze(
            asset=asset,
            factors=factors
        )


        reasoning_result = generate_reasoning(
            asset,
            signal,
            confidence,
            risk_report.risk_level.value
        )


        signals.append(
            {
                **reasoning_result,
                "risk_score": risk_report.risk_score,
                "risk_level": risk_report.risk_level.value
            }
        )


        confidence_values.append(
            confidence
        )


        risk_levels.append(
            risk_report.risk_level.value
        )



    avg_confidence = (

        sum(confidence_values)
        /
        len(confidence_values)

        if confidence_values

        else 0

    )


    risk_summary = {

        "HIGH": risk_levels.count("HIGH"),

        "MEDIUM": risk_levels.count("MEDIUM"),

        "LOW": risk_levels.count("LOW"),

        "CRITICAL": risk_levels.count("CRITICAL")

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


        "risk_intelligence": {

            "engine": "RIE",

            "status": "ACTIVE",

            "risk_summary": risk_summary

        },


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

        

    
