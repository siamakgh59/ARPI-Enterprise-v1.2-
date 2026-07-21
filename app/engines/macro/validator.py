from typing import Dict, List


class MacroValidator:
    """
    Validates macroeconomic input data
    before calculation.
    """

    def validate(
        self,
        factors: Dict[str, float | None]
    ) -> Dict:

        warnings: List[str] = []
        missing_inputs: List[str] = []

        validated_data = factors.copy()


        # Fields that should never normally be zero
        positive_required_fields = [
            "fed_rate",
            "cpi",
            "pce",
            "dxy",
            "us10y_yield"
        ]


        for field in positive_required_fields:

            value = factors.get(field)

            if value is None:
                missing_inputs.append(field)

            elif value == 0:
                warnings.append(
                    f"{field} value is suspicious"
                )

                validated_data[field] = None


        # Other optional fields

        optional_fields = [
            "nfp",
            "gold_etf_flow",
            "central_bank_gold_purchase"
        ]


        for field in optional_fields:

            if factors.get(field) is None:
                missing_inputs.append(field)


        available_inputs = sum(
            1 for value in validated_data.values()
            if value is not None
        )


        if len(warnings) > 0:
            data_quality = "INVALID"

        elif available_inputs >= 6:
            data_quality = "GOOD"

        elif available_inputs >= 3:
            data_quality = "PARTIAL"

        else:
            data_quality = "LOW"


        return {
            "validated_data": validated_data,
            "data_quality": data_quality,
            "warnings": warnings,
            "missing_inputs": missing_inputs,
            "available_inputs": available_inputs
        }
