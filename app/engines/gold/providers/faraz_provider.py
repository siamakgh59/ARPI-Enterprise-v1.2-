from datetime import datetime
from typing import Dict


class FarazGoldProvider:
    """
    Faraz.io Gold Market Data Provider

    Responsibility:
    - Fetch market data
    - Normalize fields
    - Return standard GoldData format

    No analysis should be performed here.
    """


    def __init__(self):

        self.provider_name = "Faraz.io"



    def fetch_gold_data(self) -> Dict:
        """
        Fetch latest Iran gold market data.

        Temporary mock response.
        Real API integration will replace this.
        """


        return {

            # Global Market

            "xau_usd": 3400,

            "dxy": 101,

            "us10y_yield": 4.3,


            # Iran Market

            "usd_free_rate": 950000,

            "usd_change": 0.5,

            "gold18_price": 7200000,

            "mesghal_price": 31200000,

            "coin_emami": 85000000,

            "coin_bahar": 87000000,

            "coin_bubble": 8,


            # Market Behavior

            "gold_daily_change": 0.5,

            "volume": 1000,


            "timestamp": datetime.utcnow()

        }
