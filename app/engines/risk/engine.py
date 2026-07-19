from datetime import datetime

from app.engines.risk.calculator import calculate_risk_score
from app.engines.risk.rules import classify_risk
from app.engines.risk.models import RiskReport


class RiskEngine:


    def analyze(
        self,
        asset: str,
        factors: dict
    ) -> RiskReport:


        score = calculate_risk_score(factors)


        level = classify_risk(score)


        return RiskReport(

            asset=asset,

            risk_score=score,

            risk_level=level,

            components=factors,

            confidence=90,

            timestamp=datetime.utcnow()

        )
