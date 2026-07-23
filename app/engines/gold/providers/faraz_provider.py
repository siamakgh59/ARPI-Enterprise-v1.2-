from datetime import datetime
from typing import Dict

from .faraz_scraper import FarazScraper
from .normalizer import GoldNormalizer


class FarazGoldProvider:
    """
    Faraz.io Gold Market Data Provider

    Flow:

    FarazScraper
          ↓
    Raw Data
          ↓
    GoldNormalizer
          ↓
    GoldData Format
    """


    def __init__(self):

        self.provider_name = "Faraz.io"

        self.scraper = FarazScraper()

        self.normalizer = GoldNormalizer()



    def fetch_gold_data(self) -> Dict:
        """
        Fetch and normalize gold market data.
        """


        raw_data = self.scraper.fetch_page()


        # Temporary fallback protection

        if isinstance(raw_data, dict) and "error" in raw_data:

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


        normalized_data = self.normalizer.normalize(
            raw_data
        )


        return normalized_data
