from datetime import datetime
from typing import Dict

from .faraz_scraper import FarazScraper
from .normalizer import GoldNormalizer


class FarazGoldProvider:
    """
    Faraz.io Gold Market Data Provider

    Architecture:

    FarazScraper
          |
          v
    Raw Data
          |
          v
    GoldNormalizer
          |
          v
    GoldData Schema
    """


    def __init__(self):

        self.provider_name = "Faraz.io"

        self.scraper = FarazScraper()

        self.normalizer = GoldNormalizer()



    def fetch_gold_data(self) -> Dict:
        """
        Fetch latest gold market data.

        Any external failure must not
        crash ARPI.
        """


        try:

            raw_data = self.scraper.fetch_page()


            if isinstance(raw_data, dict):

                if "error" in raw_data:

                    return self._fallback()



            normalized = self.normalizer.normalize(
                raw_data
            )


            return normalized



        except Exception as e:

            print(
                "Faraz Provider Error:",
                str(e)
            )

            return self._fallback()



    def _fallback(self) -> Dict:
        """
        Safe fallback response.
        Keeps ARPI alive when provider fails.
        """


        return {

            "xau_usd": None,

            "dxy": None,

            "us10y_yield": None,

            "usd_free_rate": None,

            "usd_change": None,

            "gold18_price": None,

            "mesghal_price": None,

            "coin_emami": None,

            "coin_bahar": None,

            "coin_bubble": None,

            "gold_daily_change": None,

            "volume": None,

            "timestamp": datetime.utcnow()

        }
