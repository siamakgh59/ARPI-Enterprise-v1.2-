from datetime import datetime
from typing import Dict


class GoldNormalizer:
    """
    Normalize external gold market data
    into ARPI GoldData format.
    """


    def normalize(
        self,
        raw_data: Dict
    ) -> Dict:
        """
        Convert scraped/provider data
        into internal Gold Engine schema.
        """


        return {

            # Global Market

            "xau_usd": raw_data.get(
                "xau_usd"
            ),

            "dxy": raw_data.get(
                "dxy"
            ),

            "us10y_yield": raw_data.get(
                "us10y_yield"
            ),


            # Iran Market

            "usd_free_rate": raw_data.get(
                "usd_free_rate"
            ),

            "usd_change": raw_data.get(
                "usd_change"
            ),

            "gold18_price": raw_data.get(
                "gold18_price"
            ),

            "mesghal_price": raw_data.get(
                "mesghal_price"
            ),

            "coin_emami": raw_data.get(
                "coin_emami"
            ),

            "coin_bahar": raw_data.get(
                "coin_bahar"
            ),

            "coin_bubble": raw_data.get(
                "coin_bubble"
            ),


            # Behavior

            "gold_daily_change": raw_data.get(
                "gold_daily_change"
            ),

            "volume": raw_data.get(
                "volume"
            ),


            "timestamp": datetime.utcnow()

        }
