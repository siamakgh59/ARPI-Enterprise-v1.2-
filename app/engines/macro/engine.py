from .models import MacroData, MacroReport
from .calculator import MacroRiskCalculator


class MacroEngine:
    """
    Core Macro Intelligence Engine
    """

    def __init__(self):
        self.calculator = MacroRiskCalculator()


    def analyze(
        self,
        data: MacroData
    ) -> MacroReport:
        """
        Analyze macro conditions
        """

        factors = data.model_dump()

        validation = self.validator.validate(factors)

result = self.calculator.calculate(
    validation["validated_data"]
)

        input_fields = [
            "fed_rate",
            "cpi",
            "pce",
            "nfp",
            "dxy",
            "us10y_yield",
            "gold_etf_flow",
            "central_bank_gold_purchase"
        ]

        available_inputs = 0
        missing_inputs = []

        for field in input_fields:
            if factors.get(field) is not None:
                available_inputs += 1
            else:
                missing_inputs.append(field)


        if available_inputs == len(input_fields):
            data_quality = "GOOD"

        elif available_inputs >= 3:
            data_quality = "PARTIAL"

        else:
            data_quality = "LOW"


        return MacroReport(
            engine="Macro Intelligence Engine",
            version="1.0.0",
            macro_score=result["macro_score"],
            macro_risk=result["macro_risk"],
            trend=result["trend"],
            confidence=result["confidence"],
            drivers=result["drivers"],
            data_quality=data_quality,
            available_inputs=available_inputs,
            missing_inputs=missing_inputs
        )
