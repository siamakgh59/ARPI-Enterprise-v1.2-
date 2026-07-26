from datetime import datetime
from typing import Dict, Any

from .scoring_engine import GoldScoringEngine



class GoldEngine:
    """
    ARPI Gold Intelligence Engine

    Sprint 3.1
    Dynamic Gold Scoring Engine

    Responsibilities:
    - Receive normalized gold data
    - Validate input availability
    - Run dynamic scoring model
    - Generate signal
    - Calculate confidence
    """


    VERSION = "3.1.0"



    def __init__(self):

        self.scoring_engine = GoldScoringEngine()



    def analyze(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze Gold Market Data
        """

        # ---------------------------------
        # Convert Pydantic Model to Dict
        # ---------------------------------

        if hasattr(data, "model_dump"):

            data = data.model_dump()



        # ---------------------------------
        # Required Inputs
        # ---------------------------------

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

            key
            for key in total_inputs
            if data.get(key) is not None

        ]



        missing_inputs = [

            key
            for key in total_inputs
            if data.get(key) is None

        ]



        available_count = len(
            available_inputs
        )


        total_count = len(
            total_inputs
        )



        # ---------------------------------
        # Data Quality
        # ---------------------------------

        if available_count == total_count:

            data_quality = "GOOD"


        elif available_count >= 5:

            data_quality = "PARTIAL"


        else:

            data_quality = "LOW"



        # ---------------------------------
        # Dynamic Gold Scoring
        # ---------------------------------

        score_result = (
            self.scoring_engine.analyze(
                data
            )
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



        # ---------------------------------
        # Trend & Signal
        # ---------------------------------

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



        # ---------------------------------
        # Confidence
        # ---------------------------------

        confidence = int(
            (
                available_count /
                total_count
            )
            *
            100
        )


        confidence = min(
            95,
            max(
                20,
                confidence
            )
        )


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



        # ---------------------------------
        # Final Report
        # ---------------------------------

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
