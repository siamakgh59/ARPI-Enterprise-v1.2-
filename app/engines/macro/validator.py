from typing import Dict, List


class MacroValidator:
    """
    Validates macroeconomic input data
    before calculation.
    """

    MACRO_FIELDS = [
        "fed_rate",
        "cpi",
        "pce",
        "nfp",
        "dxy",
        "us10y_yield",
        "gold_etf_flow",
        "central_bank_gold_purchase"
    ]


    def validate(
        self,
        factors: Dict[str, float | None]
    ) -> Dict:

        warnings: List[str] = []
        missing_inputs: List[str] = []
        invalid_inputs: List[str] = []

        validated_data = factors.copy()


        zero_sensitive_fields = [
            "fed_rate",
            "cpi",
            "pce",
            "dxy",
            "us10y_yield"
        ]


        for field in self.MACRO_FIELDS:

            value = factors.get(field)

            if value is None:
                missing_inputs.append(field)

            elif field in zero_sensitive_fields and value == 0:
                warnings.append(
                    f"{field} value is suspicious"
                )

                invalid_inputs.append(field)

                validated_data[field] = None


        valid_inputs = sum(
            1
            for field in self.MACRO_FIELDS
            if validated_data.get(field) is not None
        )


        raw_inputs = sum(
            1
            for field in self.MACRO_FIELDS
            if factors.get(field) is not None
        )


        if invalid_inputs:
            data_quality = "INVALID"

        elif valid_inputs >= 6:
            data_quality = "GOOD"

        elif valid_inputs >= 3:
            data_quality = "PARTIAL"

        else:
            data_quality = "LOW"


        return {
            "validated_data": validated_data,
            "data_quality": data_quality,
            "warnings": warnings,
            "missing_inputs": missing_inputs,
            "invalid_inputs": invalid_inputs,
            "raw_inputs": raw_inputs,
            "valid_inputs": valid_inputs,
            "available_inputs": valid_inputs
        }
