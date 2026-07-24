from datetime import datetime
from typing import Dict

import httpx

from .faraz_scraper import FarazScraper
from .faraz_parser import FarazParser
from .normalizer import GoldNormalizer



class FarazGoldProvider:
    """
    Faraz.io Gold Market Provider V7

    Sources:

    1- gold-currency
       - mesghal
       - usd
       - coins

    2- geramTalaHejdah
       - 18K gold price
    """



    def __init__(self):

        self.provider_name = "Faraz.io"

        self.scraper = FarazScraper()

        self.parser = FarazParser()

        self.normalizer = GoldNormalizer()



        self.gold18_url = (
            "https://faraz.io/markets/gold-currency/geramTalaHejdah"
        )



    def fetch_gold18_page(self):

        try:

            headers = {

                "User-Agent":
                (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )

            }


            response = httpx.get(
                self.gold18_url,
                headers=headers,
                timeout=20
            )


            response.raise_for_status()


            html = response.text


            print(
                "######## GOLD18 FETCH ########"
            )

            print(
                "URL:",
                self.gold18_url
            )

            print(
                "HTML LENGTH:",
                len(html)
            )

            print(
                "################################"
            )


            return html



        except Exception as e:


            print(
                "Gold18 Fetch Error:",
                e
            )


            return None




    def fetch_gold_data(self) -> Dict:


        try:


            print(
                "######## GOLD PROVIDER ACTIVE ########"
            )



            # -------------------------
            # SOURCE 1
            # Main Market
            # -------------------------


            market_html = (
                self.scraper.fetch_page()
            )


            if isinstance(
                market_html,
                dict
            ):

                return self._fallback()



            market_data = self.parser.parse(
                market_html,
                source="market"
            )



            print(
                "MARKET DATA:",
                market_data
            )



            # -------------------------
            # SOURCE 2
            # Gold 18
            # -------------------------


            gold18_html = (
                self.fetch_gold18_page()
            )



            gold18_data = {}



            if gold18_html:


                gold18_data = self.parser.parse(
                    gold18_html,
                    source="gold18"
                )



            print(
                "GOLD18 DATA:",
                gold18_data
            )



            # Merge

            parsed_data = {}


            parsed_data.update(
                market_data
            )


            parsed_data.update(
                gold18_data
            )



            print(
                "######## FINAL PARSED GOLD ########"
            )

            print(
                parsed_data
            )

            print(
                "###################################"
            )



            normalized = (
                self.normalizer.normalize(
                    parsed_data
                )
            )



            print(
                "NORMALIZED:",
                normalized
            )



            return normalized




        except Exception as e:


            print(
                "Faraz Provider Error:",
                e
            )


            return self._fallback()




    def _fallback(self):


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
