from datetime import datetime
from typing import Dict


class GoldNormalizer:
    """
    ARPI Gold Data Normalizer v2

    Responsibility:
    - Convert all providers output
      into Gold Engine schema
    - Preserve global market data
    - Preserve missing values safely
    """


    MESGHAL_TO_GRAM18 = 4.0715



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



        # Derive gold18 if missing

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
                data.get(
                    "coin_emami"
                ),


            "coin_bahar":
                data.get(
                    "coin_bahar"
                ),


            "coin_bubble":
                data.get(
                    "coin_bubble"
                ),



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
            "######## NORMALIZER OUTPUT ########"
        )

        print(
            normalized
        )

        print(
            "###################################"
        )



        return normalized
