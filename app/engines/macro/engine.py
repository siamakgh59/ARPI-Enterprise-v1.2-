from datetime import datetime

from app.core.base_engine import BaseEngine
from .models import MacroData, MacroReport
from .calculator import MacroRiskCalculator
from .validator import MacroValidator


class MacroEngine(BaseEngine):
    """
    ARPI Macro Intelligence Engine

    Pipeline:

    Provider
        |
    Validator
        |
    Calculator
        |
    Intelligence Report
    """

    NAME = "Macro Intelligence Engine"
    VERSION = "1.2.0"

    def __init__(self):
        self.calculator = MacroRiskCalculator()
        self.validator = MacroValidator()

    # -------------------------------------------------
    # رابط یکسان BaseEngine
    # -------------------------------------------------

    def run(self, payload: dict) -> dict:
        """
        payload یک دیکشنری خام است؛ اینجا به MacroData تبدیل و
        به analyze سپرده می‌شود تا خروجی یکسان (dict) برگردد.
        """
        macro_data = MacroData(**payload)
        report = self.analyze(macro_data)
        return report.model_dump()

    # -------------------------------------------------
    # رابط اختصاصی (بدون تغییر، برای سازگاری با کدهای فعلی)
    # -------------------------------------------------

    def analyze(self, data: MacroData) -> MacroReport:

        factors = data.model_dump()

        validation = self.validator.validate(factors)

        result = self.calculator.calculate(
            validation["validated_data"]
        )

        return MacroReport(
            engine=self.NAME,
            version=self.VERSION,
            macro_score=result.get("macro_score", 0),
            macro_risk=result.get("macro_risk", 0),
            trend=result.get("trend", "UNKNOWN"),
            confidence=result.get("confidence", 0),
            drivers=result.get("drivers", []),
            data_quality=validation.get("data_quality", "UNKNOWN"),
            available_inputs=validation.get("available_inputs", 0),
            missing_inputs=validation.get("missing_inputs", []),
            metadata={
                "warnings": validation.get("warnings", [])
            },
            timestamp=datetime.utcnow(),
        )
