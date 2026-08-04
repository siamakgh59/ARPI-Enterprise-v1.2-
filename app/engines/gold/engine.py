from datetime import datetime

from app.engines.gold.dynamic_scoring import DynamicGoldScoringEngine
from app.engines.gold.models import GoldReport

class GoldEngine:
    """
    ============================================
    ARPI Gold Intelligence Engine
    Version : 4.2.0 Stable
    ============================================

    مسئولیت‌ها:

    - اجرای Gold Calculator
    - تولید GoldReport
    - محاسبه کیفیت داده
    - محاسبه Confidence
    - تعیین Trend
    - سازگاری کامل با Dashboard
    - سازگاری کامل با Fusion Engine
    - سازگاری کامل با Swagger
    """

    VERSION = "4.2.0"

    def __init__(self):

        self.scorer = DynamicGoldScoringEngine()

    # -------------------------------------------------

    def analyze(self, data: dict):

        result = self.c
        scorer.calculate(data)

        # -----------------------------------------
        # Available Inputs
        # -----------------------------------------

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

            "volume"

        ]

        available = []

        missing = []

        for field in total_inputs:

            if data.get(field) is not None:

                available.append(field)

            else:

                missing.append(field)

        # -----------------------------------------
        # Trend Mapping
        # -----------------------------------------

        score = float(result.get("gold_score", 50))

        # -----------------------------------------
        # Trend Mapping
        # -----------------------------------------

        if score >= 85:

            trend = "STRONG_BULL"

        elif score >= 70:

            trend = "BULLISH"

        elif score >= 55:

            trend = "CAUTIOUS"

        elif score >= 40:

            trend = "SIDEWAYS"

        else:

            trend = "BEARISH"

        # -----------------------------------------
        # Signal
        # -----------------------------------------

        signal = result.get("signal", "HOLD")

        # -----------------------------------------
        # Confidence
        # -----------------------------------------

        confidence = result.get("confidence", 70)

        market_regime = result.get("market_regime")

        if market_regime == "GOLD_STRESS":

            confidence += 5

        elif market_regime == "SAFE_HAVEN":

            confidence += 3

        confidence = min(confidence, 95)

        # -----------------------------------------
        # Data Quality
        # -----------------------------------------

        if len(missing) == 0:

            data_quality = "GOOD"

        elif len(missing) <= 3:

            data_quality = "PARTIAL"

        else:

            data_quality = "WEAK"

        # -----------------------------------------
        # Drivers
        # -----------------------------------------

        drivers = result.get("drivers", [])

        # -----------------------------------------
        # Risks
        # -----------------------------------------

        risks = result.get("risks", [])

        # -----------------------------------------
        # Build Report
        # -----------------------------------------

        report = GoldReport(

            engine="Gold Intelligence Engine",

            version=self.VERSION,

            gold_score=score,

            trend=trend,

            signal=signal,

            market_regime=market_regime,

            confidence=confidence,

            drivers=drivers,

            risks=risks,

            data_quality=data_quality,

            available_inputs=len(available),

            missing_inputs=missing,

            timestamp=datetime.utcnow()

        )

        # -----------------------------------------
        # Debug
        # -----------------------------------------

        print("######## GOLD ENGINE OUTPUT ########")

        print(report.model_dump())

        print("####################################")

        return report.model_dump()

# ======================================================
# Backward Compatibility
# ======================================================

class GoldIntelligenceEngine(GoldEngine):
    """
    Legacy compatibility wrapper.

    Older parts of ARPI (Fusion Engine, Dashboard,
    API modules and previous releases) import:

        GoldIntelligenceEngine

    while newer code imports:

        GoldEngine

    This wrapper keeps both interfaces working.
    """
    pass

__all__ = [
    "GoldEngine",
    "GoldIntelligenceEngine",
]
