from typing import Dict, List


class DataQualityValidator:
    """
    ARPI Universal Data Quality Validator
    """


    def validate(
        self,
        data: Dict,
        required_fields: List[str]
    ) -> Dict:


        validated_data = data.copy()

        missing_inputs = []

        invalid_inputs = []

        warnings = []


        available_inputs = 0


        for field in required_fields:

            value = validated_data.get(field)

            if value is None:

                missing_inputs.append(field)

            else:

                available_inputs += 1



        # Positive value validation

        positive_fields = [

            "xau_usd",
            "usd_free_rate",
            "gold18_price",
            "mesghal_price",
            "coin_emami",
            "coin_bahar"

        ]


        for field in positive_fields:

            value = validated_data.get(field)

            if value is not None and value <= 0:

                invalid_inputs.append(field)

                warnings.append(
                    f"{field} value is invalid"
                )

                validated_data[field] = None



        # Bubble validation

        bubble = validated_data.get(
            "coin_bubble"
        )


        if bubble is not None and bubble < 0:

            invalid_inputs.append(
                "coin_bubble"
            )

            warnings.append(
                "Negative coin bubble detected"
            )

            validated_data["coin_bubble"] = None



        available_inputs = sum(

            1
            for field in required_fields
            if validated_data.get(field) is not None

        )


        if invalid_inputs:

            data_quality = "INVALID"

        else:

            ratio = (
                available_inputs /
                len(required_fields)
            )


            if ratio >= 0.85:

                data_quality = "GOOD"

            elif ratio >= 0.50:

                data_quality = "PARTIAL"

            else:

                data_quality = "LOW"



        return {

            "validated_data": validated_data,

            "available_inputs": available_inputs,

            "missing_inputs": missing_inputs,

            "invalid_inputs": invalid_inputs,

            "warnings": warnings,

            "data_quality": data_quality

        }
