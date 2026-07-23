from .models import GoldData, GoldReport
from .validator import GoldValidator
from .calculator import GoldCalculator


class GoldEngine:
    """
    Core Gold Intelligence Engine

    Flow:

    GoldData
        ↓
    Validator
        ↓
    Calculator
        ↓
    GoldReport
    """


    def __init__(self):

        self.validator = GoldValidator()

        self.calculator = GoldCalculator()



    def analyze(
        self,
        data: GoldData
    ) -> GoldReport:
        """
        Analyze gold market conditions
        """


        factors = data.model_dump()


        validation = self.validator.validate(
            factors
        )


        result = self.calculator.calculate(
            validation["validated_data"]
        )


        return GoldReport(

            engine="Gold Intelligence Engine",

            version="1.0.0",

            gold_score=result["gold_score"],

            trend=result["trend"],

            signal=result["signal"],

            confidence=result["confidence"],

            drivers=result["drivers"],

            risks=result["risks"],

            data_quality=validation["data_quality"],

            available_inputs=validation["available_inputs"],

            missing_inputs=validation["missing_inputs"]

        )
