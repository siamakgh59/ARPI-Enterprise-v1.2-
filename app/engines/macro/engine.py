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

        result = self.calculator.calculate(
            data.model_dump()
        )


        return MacroReport(
            engine="Macro Intelligence Engine",
            version="1.0.0",
            macro_score=result["macro_score"],
            macro_risk=result["macro_risk"],
            trend=result["trend"],
            confidence=result["confidence"],
            drivers=result["drivers"]
        )
