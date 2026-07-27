from datetime import datetime
from typing import Dict

import httpx

from ..faraz_scraper import FarazScraper
from ..faraz_parser import FarazParser
from ..coin_parser import CoinParser
from ..normalizer import GoldNormalizer


class FarazGoldProvider:
    """
    ARPI Gold Intelligence Provider

    Version:
        V10.0

    Sources:

    Main:
        gold-currency
            - mesghal_price
            - usd_free_rate
            - usd_change
            - gold_daily_change

    Coin:
        gold-currency?page=2
            - coin_emami
            - coin_bahar
            - coin_bubble

    Gold18:
        geramTalaHejdah
            - gold18_price
            - volume
    """

    VERSION = "10.0.0"


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

        try:

            headers = {

                "User-Agent":
                    (
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64)"
                    )

            }


            response = httpx.get(
                url,
                headers=headers,
                timeout=20
            )


            response.raise_for_status()


            return response.text


        except Exception as e:

            print(
                "FETCH ERROR:",
                url,
                e
            )

            return None



    def fetch_coin_page(self):

        print(
            "######## COIN FETCH ########"
        )

        html = self.fetch_page(
            self.coin_url
        )


        if html:

            print(
                "COIN HTML LENGTH:",
                len(html)
            )


        return html



    def fetch_gold18_page(self):

        print(
            "######## GOLD18 FETCH ########"
        )


        html = self.fetch_page(
            self.gold18_url
        )


        if html:

            print(
                "GOLD18 HTML LENGTH:",
                len(html)
            )


        return html



    def fetch_gold_data(
        self
    ) -> Dict:


        try:

            print(
                "######## GOLD PROVIDER ACTIVE ########"
            )


            parsed_data = {}



            # ----------------------------
            # Main Market
            # ----------------------------

            market_html = (
                self.scraper.fetch_page()
            )


            if market_html:

                market_data = (
                    self.parser.parse(
                        market_html,
                        source="market"
                    )
                )

                parsed_data.update(
                    market_data
                )


                print(
                    "MARKET DATA:",
                    market_data
                )



            # ----------------------------
            # Coin
            # ----------------------------

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


                parsed_data.update(
                    coin_data
                )


                print(
                    "COIN DATA:",
                    coin_data
                )



            # ----------------------------
            # Gold18
            # ----------------------------

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


                parsed_data.update(
                    gold18_data
                )


                print(
                    "GOLD18 DATA:",
                    gold18_data
                )



            # ----------------------------
            # Normalize coin bubble
            # ----------------------------

            coin = parsed_data.get(
                "coin_emami"
            )


            mesghal = parsed_data.get(
                "mesghal_price"
            )


            if coin and mesghal:

                theoretical = (
                    mesghal * 0.235
                )


                bubble = (
                    (
                        coin - theoretical
                    )
                    /
                    theoretical
                ) * 100


                parsed_data[
                    "coin_bubble"
                ] = round(
                    bubble,
                    2
                )


                print(
                    "CALCULATED BUBBLE:",
                    bubble
                )



            print(
                "######## FINAL GOLD DATA ########"
            )

            print(
                parsed_data
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
                "FARAZ PROVIDER ERROR:",
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
