from fastapi import APIRouter

from app.engines.risk.engine import RiskEngine
from app.engines.risk.adapter import build_risk_factors


risk_router = APIRouter(
    prefix="/risk",
    tags=["Risk Intelligence Engine"]
)


engine = RiskEngine()


@risk_router.get("/analyze/{asset}")
def analyze_risk(asset: str):

    market_data = {

        "confidence": 75,

        "risk": "MEDIUM"

    }


    factors = build_risk_factors(
        market_data
    )


    report = engine.analyze(
        asset,
        factors
    )


    return report

        

    
