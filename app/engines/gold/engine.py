from datetime import datetime
from typing import Dict, Any

from .validator import GoldValidator
from .calculator import GoldCalculator


class GoldIntelligenceEngine:

    """
    ARPI Gold Intelligence Engine v3.3

    Pipeline:

    Provider
        |
    Normalizer
        |
    Validator
        |
    Calculator
        |
    Intelligence Report

    """

    VERSION = "3.3.0"


    def __init__(self):

        self.validator = GoldValidator()

        self.calculator = GoldCalculator()



    def analyze(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:


        validation = (
            self.validator.validate(
                data
            )
        )


        validated_data = (
            validation["validated_data"]
        )


        result = (
            self.calculator.calculate(
                validated_data
            )
        )


        print(
            "######## ACTIVE GOLD CALCULATOR ########"
        )

        print(
            result.get(
                "calculator_version"
            )
        )

        print(
            "########################################"
        )



        return {


            "engine":
                "Gold Intelligence Engine",


            "version":
                self.VERSION,


            "gold_score":
                result["gold_score"],


            "trend":
                result["trend"],


            "signal":
                result["signal"],


            "confidence":
                result["confidence"],


            "drivers":
                result["drivers"],


            "risks":
                result["risks"],


            "data_quality":
                validation["data_quality"],


            "available_inputs":
                validation["available_inputs"],


            "missing_inputs":
                validation["missing_inputs"],


            "timestamp":
                datetime.utcnow()

        }
