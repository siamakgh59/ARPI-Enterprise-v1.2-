from fastapi import APIRouter

from app.engines.risk.engine import RiskEngine
from app.engines.risk.market_adapter import market_to_risk_factors
from app.market import market_live


risk_router = APIRouter(
    prefix="/risk",
    tags=["Risk Intelligence Engine"]
)


engine = RiskEngine()


@risk_router.get("/analyze/{asset}")
def analyze_risk(asset: str):

    market_data = market_live()

    analysis = market_data.get(
        "analysis",
        {}
    )


    asset_analysis = analysis.get(
        asset,
        {}
    )


    factors = market_to_risk_factors(
        asset_analysis
    )


    report = engine.analyze(
        asset=asset,
        factors=factors
    )


    return report
