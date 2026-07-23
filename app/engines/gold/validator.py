from typing import Dict, List


class GoldValidator:
    """
    Validates gold intelligence input data
    before calculation.
    """


    GOLD_FIELDS = [

        "xau_usd",

        "gold_daily_change",

        "usd_irr",

        "gold18_price",

        "mesghal_price",

        "coin_emami",

        "coin_bahar",

        "coin_bubble",

        "gold_etf_flow",

        "central_bank_gold_purchase",

        "dxy",

        "us10y_yield"

    ]


    def validate(
        self,
        factors: Dict[str, float | None]
    ) -> Dict:


        warnings: List[str] = []

        missing_inputs: List[str] = []

        invalid_inputs: List[str] = []


        validated_data = factors.copy()


        # Detect missing values

        for field in self.GOLD_FIELDS:

            value = factors.get(field)

            if value is None:

                missing_inputs.append(field)



        # Validate prices

        positive_fields = [

            "xau_usd",

            "usd_irr",

            "gold18_price",

            "mesghal_price",

            "coin_emami",

            "coin_bahar"

        ]


        for field in positive_fields:

            value = factors.get(field)


            if value is not None and value <= 0:

                warnings.append(
                    f"{field} value is invalid"
                )

                invalid_inputs.append(field)

                validated_data[field] = None



        # Validate bubble

        bubble = factors.get(
            "coin_bubble"
        )


        if bubble is not None:

            if bubble < 0:

                warnings.append(
                    "Negative coin bubble detected"
                )

                invalid_inputs.append(
                    "coin_bubble"
                )

                validated_data["coin_bubble"] = None



        valid_inputs = sum(

            1

            for field in self.GOLD_FIELDS

            if validated_data.get(field) is not None

        )



        if invalid_inputs:

            data_quality = "INVALID"

        elif valid_inputs >= 8:

            data_quality = "GOOD"

        elif valid_inputs >= 4:

            data_quality = "PARTIAL"

        else:

            data_quality = "LOW"



        return {

            "validated_data": validated_data,

            "data_quality": data_quality,

            "available_inputs": valid_inputs,

            "missing_inputs": missing_inputs,

            "invalid_inputs": invalid_inputs,

            "warnings": warnings

        }
