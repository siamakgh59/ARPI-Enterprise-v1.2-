from app.core.data_quality.validator import DataQualityValidator


class GoldValidator:

    GOLD_FIELDS = [

        "xau_usd",
        "dxy",
        "us10y_yield",

        "usd_free_rate",
        "usd_change",

        "gold18_price",
        "mesghal_price",

        "coin_emami",
        "coin_bahar",
        "coin_bubble",

        "gold_daily_change",
        "volume"

    ]


    def __init__(self):

        self.validator = DataQualityValidator()



    def validate(
        self,
        data: dict
    ):

        return self.validator.validate(

            data,

            self.GOLD_FIELDS

        )
