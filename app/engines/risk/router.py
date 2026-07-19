from fastapi import APIRouter

from app.engines.risk.engine import RiskEngine


risk_router = APIRouter(
    prefix="/risk",
    tags=["Risk Intelligence Engine"]
)


engine = RiskEngine()


@risk_router.get("/analyze/{asset}")
def analyze_risk(asset: str):

    sample_factors = {

        "market_risk": 70,

        "volatility_risk": 80,

        "macro_risk": 60,

        "liquidity_risk": 40,

        "geopolitical_risk": 90,

        "data_confidence_risk": 20

    }


    report = engine.analyze(
        asset=asset,
        factors=sample_factors
    )


    return report
