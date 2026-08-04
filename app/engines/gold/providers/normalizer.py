from datetime import datetime
from typing import Dict


class GoldNormalizer:
    """
    ARPI Gold Data Normalizer v4.1

    Responsibilities:
    - Convert providers output
      into Gold Engine schema
    - Preserve global market data
    - Preserve missing values safely
    - Calculate derived intelligence indicators

    Added:
    - coin_bubble_percent
      for normalized bubble risk analysis
    """


    MESGHAL_TO_GRAM18 = 4.0715


    VERSION = "4.1.0"



    def normalize(
        self,
        raw_data: Dict
    ) -> Dict:


        data = raw_data or {}



        mesghal_price = data.get(
            "mesghal_price"
        )


        gold18_price = data.get(
            "gold18_price"
        )



        # --------------------------------
        # Derive Gold18 price if missing
        # --------------------------------

        if (
            gold18_price is None
            and
            mesghal_price is not None
        ):

            try:

                gold18_price = round(
                    mesghal_price
                    /
                    self.MESGHAL_TO_GRAM18
                )


            except Exception:

                gold18_price = None



        coin_emami = data.get(
            "coin_emami"
        )


        coin_bubble = data.get(
            "coin_bubble"
        )



        # --------------------------------
        # Smart Coin Bubble Calculation
        # --------------------------------

        coin_bubble_percent = None


        if (
            coin_bubble is not None
            and
            coin_emami is not None
            and
            coin_emami > 0
        ):

            try:

                coin_bubble_percent = round(

                    (
                        coin_bubble
                        /
                        coin_emami
                    )
                    *
                    100,

                    2

                )


            except Exception:

                coin_bubble_percent = None



        normalized = {


            # =====================
            # Global Market
            # =====================

            "xau_usd":
                data.get(
                    "xau_usd"
                ),


            "dxy":
                data.get(
                    "dxy"
                ),


            "us10y_yield":
                data.get(
                    "us10y_yield"
                ),



            # =====================
            # Iran Market
            # =====================

            "usd_free_rate":
                data.get(
                    "usd_free_rate"
                ),


            "usd_change":
                data.get(
                    "usd_change"
                ),


            "gold18_price":
                gold18_price,


            "mesghal_price":
                mesghal_price,


            "coin_emami":
                coin_emami,


            "coin_bahar":
                data.get(
                    "coin_bahar"
                ),


            "coin_bubble":
                coin_bubble,


            "coin_bubble_percent":
                coin_bubble_percent,



            # =====================
            # Market Behavior
            # =====================

            "gold_daily_change":
                data.get(
                    "gold_daily_change"
                ),


            "volume":
                data.get(
                    "volume"
                ),


            "timestamp":
                datetime.utcnow()

        }



        print(
            "######## NORMALIZER v4.1 OUTPUT ########"
        )

        print(
            normalized
        )

        print(
            "########################################"
        )



        return normalized
