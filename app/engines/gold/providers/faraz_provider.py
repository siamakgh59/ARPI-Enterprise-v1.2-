from datetime import datetime
from typing import Dict

from .faraz_scraper import FarazScraper
from .faraz_parser import FarazParser
from .normalizer import GoldNormalizer


class FarazGoldProvider:
    """
    Faraz.io Gold Market Data Provider

    Architecture:

    FarazScraper
          |
          v
    Raw HTML
          |
          v
    FarazParser
          |
          v
    Parsed Data
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

        self.parser = FarazParser()

        self.normalizer = GoldNormalizer()



    def fetch_gold_data(self) -> Dict:
        """
        Fetch latest gold market data.
        External failures must not crash ARPI.
        """


        try:

            raw_html = self.scraper.fetch_page()


            if isinstance(raw_html, dict):

                if "error" in raw_html:

                    return self._fallback()



            parsed_data = self.parser.parse(
                raw_html
            )


            print(
                "######## FARAZ PARSED DATA ########"
            )

            print(
                parsed_data
            )

            print(
                "###################################"
            )


            normalized = self.normalizer.normalize(
                parsed_data
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
        Keeps ARPI alive.
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
