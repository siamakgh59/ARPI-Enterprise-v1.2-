from typing import Dict, List


class GoldValidator:
    """
    Validates gold intelligence input data
    before calculation.
    """


    GOLD_FIELDS = [

        # Global Market

        "xau_usd",

        "dxy",

        "us10y_yield",


        # Iran Market

        "usd_free_rate",

        "usd_change",

        "gold18_price",

        "mesghal_price",

        "coin_emami",

        "coin_bahar",

        "coin_bubble",


        # Market Behavior

        "gold_daily_change",

        "volume"

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



        # Validate positive values

        positive_fields = [

            "xau_usd",

            "usd_free_rate",

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



        # Validate coin bubble

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



        # Count valid inputs

        valid_inputs = sum(

            1

            for field in self.GOLD_FIELDS

            if validated_data.get(field) is not None

        )



        # Debug Log

        print(
            "######## GOLD VALIDATION DEBUG ########"
        )

        print(
            {
                "available_inputs": valid_inputs,
                "missing_inputs": missing_inputs,
                "invalid_inputs": invalid_inputs,
                "warnings": warnings
            }
        )

        print(
            "########################################"
        )



        # Quality Classification

        if invalid_inputs:

            data_quality = "INVALID"

        elif valid_inputs >= 8:

            data_quality = "GOOD"

        elif valid_inputs >= 5:

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
