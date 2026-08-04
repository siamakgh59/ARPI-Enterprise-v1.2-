from datetime import datetime
from typing import Dict
import time

import httpx

from .faraz_scraper import FarazScraper
from .faraz_parser import FarazParser
from .coin_parser import CoinParser
from .normalizer import GoldNormalizer


class FarazGoldProvider:
    """
    Faraz.io Gold Market Provider V11

    Sources:

    1- gold-currency
       - mesghal
       - usd

    2- gold-currency?page=2
       - coin_emami
       - coin_bahar
       - coin_bubble

    3- geramTalaHejdah
       - gold18
       - volume
    """


    def __init__(self):

        self.provider_name = "Faraz.io"

        self.scraper = FarazScraper()

        self.parser = FarazParser()

        self.coin_parser = CoinParser()

        self.normalizer = GoldNormalizer()


        self.coin_url = (
            "https://faraz.io/markets/gold-currency?page=2"
        )


        self.gold18_url = (
            "https://faraz.io/markets/gold-currency/geramTalaHejdah"
        )



    def fetch_page(
        self,
        url: str
    ):


        headers = {

            "User-Agent":
                (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )

        }



        for attempt in range(3):

            try:


                response = httpx.get(

                    url,

                    headers=headers,

                    timeout=httpx.Timeout(
                        connect=10,
                        read=40,
                        write=10,
                        pool=10
                    )

                )


                response.raise_for_status()


                return response.text



            except Exception as e:


                print(
                    f"FETCH ATTEMPT {attempt + 1}/3 FAILED:",
                    url,
                    e
                )


                time.sleep(2)



        print(
            "FETCH FAILED AFTER RETRIES:",
            url
        )


        return None



    def fetch_coin_page(self):

        print(
            "######## COIN FETCH ########"
        )


        print(
            "URL:",
            self.coin_url
        )


        html = self.fetch_page(
            self.coin_url
        )


        if html:

            print(
                "COIN HTML LENGTH:",
                len(html)
            )


        print(
            "############################"
        )


        return html



    def fetch_gold18_page(self):

        print(
            "######## GOLD18 FETCH ########"
        )


        print(
            "URL:",
            self.gold18_url
        )


        html = self.fetch_page(
            self.gold18_url
        )


        if html:

            print(
                "HTML LENGTH:",
                len(html)
            )


        print(
            "################################"
        )


        return html



    def fetch_gold_data(
        self
    ) -> Dict:


        try:


            print(
                "######## GOLD PROVIDER ACTIVE ########"
            )



            market_html = (
                self.scraper.fetch_page()
            )


            if isinstance(
                market_html,
                dict
            ):

                return self._fallback()



            market_data = (
                self.parser.parse(
                    market_html,
                    source="market"
                )
            )


            print(
                "MARKET DATA:",
                market_data
            )



            coin_data = {}


            coin_html = (
                self.fetch_coin_page()
            )


            if coin_html:


                coin_data = (
                    self.coin_parser.parse(
                        coin_html,
                        source="coin"
                    )
                )


            print(
                "COIN DATA:",
                coin_data
            )



            gold18_data = {}


            gold18_html = (
                self.fetch_gold18_page()
            )


            if gold18_html:


                gold18_data = (
                    self.parser.parse(
                        gold18_html,
                        source="gold18"
                    )
                )


            print(
                "GOLD18 DATA:",
                gold18_data
            )



            parsed_data = {}


            parsed_data.update(
                market_data
            )


            parsed_data.update(
                coin_data
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


            "timestamp":
                datetime.utcnow()

        }
