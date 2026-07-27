class MacroEngine:
    """
    Core Macro Intelligence Engine v1.2
    """

    VERSION = "1.2.0"


    def __init__(self):

        self.calculator = MacroRiskCalculator()

        self.validator = MacroValidator()


    def analyze(
        self,
        data: MacroData
    ) -> MacroReport:


        factors = data.model_dump()


        validation = self.validator.validate(
            factors
        )


        result = self.calculator.calculate(
            validation["validated_data"]
        )


        return MacroReport(

            engine="Macro Intelligence Engine",

            version=self.VERSION,

            macro_score=result["macro_score"],

            macro_risk=result["macro_risk"],

            trend=result["trend"],

            confidence=result["confidence"],

            drivers=result["drivers"],

            data_quality=validation["data_quality"],

            available_inputs=validation["available_inputs"],

            missing_inputs=validation["missing_inputs"],

            metadata={

                "warnings":
                    validation["warnings"],

                "source":
                    "Macro Intelligence Engine",

                "factor_count":
                    len(validation["validated_data"])

            }
        )
