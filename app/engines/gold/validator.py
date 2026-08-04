from datetime import datetime

from app.core.data_quality.validator import DataQualityValidator



class GoldValidator:

    """
    ARPI Gold Validator v3.4

    Responsibilities:

    - Validate Gold Engine inputs
    - Maintain Gold schema
    - Delegate quality scoring
      to Core DataQuality Engine

    """



    VERSION = "3.4.0"



    GOLD_FIELDS = [

        # Global Market

        "xau_usd",
        "dxy",
        "us10y_yield",


        # Iran Market

        "usd_free_rate",
        "usd_change",


        # Gold Market

        "gold18_price",
        "mesghal_price",


        # Coin Market

        "coin_emami",
        "coin_bahar",
        "coin_bubble",


        # Behaviour

        "gold_daily_change",
        "volume"

    ]



    def __init__(self):

        self.validator = DataQualityValidator()



    def validate(
        self,
        data: dict
    ):


        result = self.validator.validate(

            data,

            self.GOLD_FIELDS

        )



        # Add Gold Engine metadata

        result[
            "validator_version"
        ] = self.VERSION



        result[
            "validated_at"
        ] = datetime.utcnow()



        return result
