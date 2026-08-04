from typing import Dict, List


class DataQualityValidator:
    """
    ARPI Universal Data Quality Validator

    Used by:
    - Macro Intelligence Engine
    - Gold Intelligence Engine
    - Risk Intelligence Engine
    """


    def validate(
        self,
        data: Dict,
        required_fields: List[str]
    ) -> Dict:


        missing_inputs = []

        available_inputs = 0


        for field in required_fields:

            value = data.get(field)


            if value is None:

                missing_inputs.append(
                    field
                )

            else:

                available_inputs += 1



        total_inputs = len(
            required_fields
        )


        quality = self.calculate_quality(
            available_inputs,
            total_inputs
        )


        return {

            "available_inputs":
                available_inputs,

            "missing_inputs":
                missing_inputs,

            "data_quality":
                quality,

            "validated_data":
                data,

            "warnings":
                []

        }



    def calculate_quality(
        self,
        available: int,
        total: int
    ) -> str:


        if total == 0:

            return "UNKNOWN"


        ratio = (
            available /
            total
        )


        if ratio >= 0.85:

            return "GOOD"


        elif ratio >= 0.50:

            return "MEDIUM"


        else:

            return "LOW"
