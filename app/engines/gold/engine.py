from datetime import datetime

from app.engines.gold.calculator import GoldCalculator
from app.engines.gold.models import GoldReport


class GoldEngine:
    """
    ARPI Gold Intelligence Engine v4.2
    """

    VERSION = "4.2.0"

    def __init__(self):
        self.calculator = GoldCalculator()

    def analyze(self, data: dict):

        result = self.calculator.calculate(data)

        # -----------------------------
        # Available Inputs
        # -----------------------------

        total_inputs = [
            "xau_usd",
            "dxy",
            "us10y_yield",
            "usd_free_rate",
            "usd_change",
            "gold18_price",
            "mesghal_price",
            "coin_emami",
            "coin_bahar",
            "coin_bubble",
            "gold_daily_change",
            "volume",
        ]

        available = []
        missing = []

        for field in total_inputs:
            if data.get(field) is not None:
                available.append(field)
            else:
                missing.append(field)

        # -----------------------------
        # Trend
        # -----------------------------

        score = result["gold_score"]

        if score >= 85:
            trend = "STRONG_BULL"

        elif score >= 70:
            trend = "CAUTIOUS"

        elif score >= 55:
            trend = "SIDEWAYS"

        else:
            trend = "BEARISH"

        # -----------------------------
        # Confidence
        # -----------------------------

        confidence = result.get("confidence", 70)

        if result.get("market_regime") == "GOLD_STRESS":
            confidence += 5

        confidence = min(95, confidence)

        # -----------------------------
        # Report
        # -----------------------------

        report = GoldReport(

            engine="Gold Intelligence Engine",

            version=self.VERSION,

            gold_score=score,

            trend=trend,

            signal=result["signal"],

            market_regime=result.get("market_regime"),

            confidence=confidence,

            drivers=result["drivers"],

            risks=result["risks"],

            data_quality="GOOD" if len(missing) == 0 else "PARTIAL",

            available_inputs=len(available),

            missing_inputs=missing,

            timestamp=datetime.utcnow()

        )

        return report.model_dump()
