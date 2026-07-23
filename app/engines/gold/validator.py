from typing import Dict, List


class GoldValidator:
    """
    Validates gold market input data
    before calculation.
    """


    GOLD_FIELDS = [

        "xau_usd",

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


        # بررسی داده‌های ضروری

        critical_fields = [

            "xau_usd",

            "usd_irr",

            "gold18_price"

        ]


        for field in self.GOLD_FIELDS:


            value = factors.get(field)


            if value is None:

                missing_inputs.append(field)


        # کنترل مقادیر غیرمنطقی

        if factors.get("xau_usd") is not None:

            if factors["xau_usd"] <= 0:

                warnings.append(
                    "Invalid XAU/USD price"
                )

                invalid_inputs.append(
                    "xau_usd"
                )

                validated_data["xau_usd"] = None



        if factors.get("usd_irr") is not None:

            if factors["usd_irr"] <= 0:

                warnings.append(
                    "Invalid USD/IRR price"
                )

                invalid_inputs.append(
                    "usd_irr"
                )

                validated_data["usd_irr"] = None



        # کیفیت داده

        valid_inputs = sum(

            1

            for field in self.GOLD_FIELDS

            if validated_data.get(field) is not None

        )


        total_inputs = len(
            self.GOLD_FIELDS
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
