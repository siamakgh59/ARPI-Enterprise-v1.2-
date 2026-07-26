from datetime import datetime
from typing import Dict, Any

from .validator import GoldValidator
from .calculator import GoldCalculator
from .scoring_engine import GoldScoringEngine


class GoldIntelligenceEngine:
    """
    ARPI Gold Intelligence Engine

    Sprint 3
    Dynamic Gold Scoring Engine

    Pipeline:

    Provider
        |
    Normalizer
        |
    Validator
        |
    Calculator
        |
    Scoring Engine
        |
    Signal Output
    """

    VERSION = "3.2.0"


    def __init__(self):

        self.validator = GoldValidator()

        self.calculator = GoldCalculator()

        self.scoring_engine = GoldScoringEngine()



    def analyze(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Main Gold Intelligence Pipeline
        """


        # -----------------------------
        # Validation
        # -----------------------------

        validation = self.validator.validate(
            data
        )


        validated_data = validation[
            "validated_data"
        ]



        # -----------------------------
        # Dynamic Calculation
        # -----------------------------

        calculation = self.calculator.calculate(
            validated_data
        )



        # -----------------------------
        # Weighted Scoring
        # -----------------------------

        scoring = self.scoring_engine.analyze(
            validated_data
        )



        # Final score fusion

        calculator_score = calculation[
            "gold_score"
        ]

        weighted_score = scoring[
            "gold_score"
        ]


        final_score = round(
            (
                calculator_score * 0.6
                +
                weighted_score * 0.4
            ),
            2
        )



        # -----------------------------
        # Signal
        # -----------------------------

        if final_score >= 80:

            signal = "STRONG BUY"
            trend = "BULLISH"


        elif final_score >= 65:

            signal = "BUY"
            trend = "BULLISH"


        elif final_score <= 35:

            signal = "SELL"
            trend = "BEARISH"


        else:

            signal = "HOLD"
            trend = "NEUTRAL"



        # -----------------------------
        # Confidence
        # -----------------------------

        confidence = validation[
            "available_inputs"
        ] / len(
            self.validator.GOLD_FIELDS
        ) * 100


        confidence = round(
            min(
                95,
                max(
                    20,
                    confidence
                )
            )
        )



        return {

            "engine":
                "Gold Intelligence Engine",


            "version":
                self.VERSION,


            "gold_score":
                final_score,


            "trend":
                trend,


            "signal":
                signal,


            "confidence":
                confidence,


            "drivers":
                list(
                    set(
                        calculation["drivers"]
                        +
                        scoring["drivers"]
                    )
                ),


            "risks":
                list(
                    set(
                        calculation["risks"]
                        +
                        scoring["risks"]
                    )
                ),


            "factor_scores":
                scoring.get(
                    "factor_scores",
                    {}
                ),


            "calculator_score":
                calculator_score,


            "weighted_score":
                weighted_score,


            "data_quality":
                validation[
                    "data_quality"
                ],


            "available_inputs":
                validation[
                    "available_inputs"
                ],


            "missing_inputs":
                validation[
                    "missing_inputs"
                ],


            "invalid_inputs":
                validation[
                    "invalid_inputs"
                ],


            "warnings":
                validation[
                    "warnings"
                ],


            "timestamp":
                datetime.utcnow()

        }
