from app.engines.risk.config import RISK_WEIGHTS


def calculate_risk_score(factors: dict) -> float:

    score = 0

    for factor, weight in RISK_WEIGHTS.items():

        value = factors.get(factor, 0)

        score += value * weight

    return round(score, 2)
