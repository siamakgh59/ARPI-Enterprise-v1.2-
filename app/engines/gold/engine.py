from datetime import datetime
from typing import Dict, Any, List

from app.engines.gold.scoring import GoldScoringEngine


class GoldIntelligenceEngine:
    """
    ARPI Gold Intelligence Engine

    Responsible for:
    - Gold market intelligence
    - Score calculation
    - Signal generation
    - Confidence estimation
    - Data quality awareness
    """


    VERSION = "2.0.0"


    def __init__(self):
        self.scorer = GoldScoringEngine()


    def analyze(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze normalized gold data.
        """

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


        available_inputs = [
            key for key in total_inputs
            if data.get(key) is not None
        ]


        missing_inputs = [
            key for key in total_inputs
            if data.get(key) is None
        ]


        available_count = len(
            available_inputs
        )


        total_count = len(
            total_inputs
        )


        # -----------------------------
        # Data Quality
        # -----------------------------

        if available_count == total_count:

            data_quality = "GOOD"

        elif available_count >= 5:

            data_quality = "PARTIAL"

        else:

            data_quality = "LOW"



        # -----------------------------
        # Core Scoring
        # -----------------------------

        try:

            score_result = self.scorer.analyze(
                data
            )


            gold_score = score_result.get(
                "gold_score",
                50
            )


            drivers = score_result.get(
                "drivers",
                []
            )


            risks = score_result.get(
                "risks",
                []
            )


        except Exception as e:

            gold_score = 50

            drivers = []

            risks = [
                f"scoring_error:{str(e)}"
            ]



        # -----------------------------
        # Signal Logic
        # -----------------------------

        if gold_score >= 80:

            signal = "STRONG BUY"

            trend = "BULLISH"


        elif gold_score >= 65:

            signal = "BUY"

            trend = "BULLISH"


        elif gold_score <= 35:

            signal = "SELL"

            trend = "BEARISH"


        else:

            signal = "HOLD"

            trend = "NEUTRAL"



        # -----------------------------
        # Confidence Model
        # -----------------------------

        base_confidence = (
            available_count /
            total_count
        ) * 100


        confidence = int(
            min(
                95,
                max(
                    20,
                    base_confidence
                )
            )
        )


        # کاهش اعتماد در دیتای ناقص

        if data_quality == "LOW":

            confidence = min(
                confidence,
                40
            )


        elif data_quality == "PARTIAL":

            confidence = min(
                confidence,
                70
            )



        return {

            "engine":
                "Gold Intelligence Engine",


            "version":
                self.VERSION,


            "gold_score":
                round(
                    gold_score,
                    2
                ),


            "trend":
                trend,


            "signal":
                signal,


            "confidence":
                confidence,


            "drivers":
                drivers,


            "risks":
                risks,


            "data_quality":
                data_quality,


            "available_inputs":
                available_count,


            "missing_inputs":
                missing_inputs,


            "available_fields":
                available_inputs,


            "timestamp":
                datetime.utcnow()

        }
