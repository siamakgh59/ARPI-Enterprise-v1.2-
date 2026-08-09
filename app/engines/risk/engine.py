from datetime import datetime

from app.core.base_engine import BaseEngine
from app.engines.risk.calculator import calculate_risk_score
from app.engines.risk.rules import classify_risk
from app.engines.risk.models import RiskReport


class RiskEngine(BaseEngine):

    NAME = "Risk Intelligence Engine"
    VERSION = "1.0.0"

    # -------------------------------------------------
    # رابط یکسان BaseEngine
    # -------------------------------------------------

    def run(self, payload: dict) -> dict:
        """
        payload انتظار می‌رود شامل کلید 'asset' باشد؛ بقیه‌ی کلیدها
        به‌عنوان factors به analyze پاس داده می‌شوند.
        اگر 'asset' در payload نباشد، مقدار پیش‌فرض 'UNKNOWN' استفاده می‌شود.
        """
        asset = payload.get("asset", "UNKNOWN")
        factors = payload.get("factors", payload)

        report = self.analyze(asset=asset, factors=factors)
        return report.model_dump()

    # -------------------------------------------------
    # رابط اختصاصی (بدون تغییر، برای سازگاری با کدهای فعلی)
    # -------------------------------------------------

    def analyze(self, asset: str, factors: dict) -> RiskReport:

        score = calculate_risk_score(factors)

        level = classify_risk(score)

        return RiskReport(
            asset=asset,
            risk_score=score,
            risk_level=level,
            components=factors,
            confidence=90,
            timestamp=datetime.utcnow(),
        )
