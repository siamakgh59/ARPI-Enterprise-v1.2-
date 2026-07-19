from app.engines.risk.models import RiskLevel


def classify_risk(score: float) -> RiskLevel:

    if score >= 85:
        return RiskLevel.CRITICAL

    if score >= 65:
        return RiskLevel.HIGH

    if score >= 35:
        return RiskLevel.MEDIUM

    return RiskLevel.LOW
