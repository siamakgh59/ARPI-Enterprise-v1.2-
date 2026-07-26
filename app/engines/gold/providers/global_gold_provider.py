from datetime import datetime
from typing import Dict

import yfinance as yf


class GlobalGoldProvider:
    """
    ARPI Global Gold Provider V1

    Sources:
    - XAU/USD
    - DXY
    - US10Y Yield
    """


    def __init__(self):

        self.provider_name = "Global Market Provider"



    def fetch_global_data(self) -> Dict:

        print(
            "######## GLOBAL GOLD PROVIDER ACTIVE ########"
        )


        try:

            result = {

                "xau_usd": None,

                "dxy": None,

                "us10y_yield": None,

                "timestamp": datetime.utcnow()

            }


            # -------------------------
            # Gold Spot
            # -------------------------

            gold = yf.Ticker(
                "GC=F"
            )


            gold_data = gold.history(
                period="1d"
            )


            if not gold_data.empty:

                result[
                    "xau_usd"
                ] = round(
                    float(
                        gold_data["Close"].iloc[-1]
                    ),
                    2
                )



            # -------------------------
            # Dollar Index
            # -------------------------

            dxy = yf.Ticker(
                "DX-Y.NYB"
            )


            dxy_data = dxy.history(
                period="1d"
            )


            if not dxy_data.empty:

                result[
                    "dxy"
                ] = round(
                    float(
                        dxy_data["Close"].iloc[-1]
                    ),
                    2
                )



            # -------------------------
            # US 10Y Yield
            # -------------------------

            us10y = yf.Ticker(
                "^TNX"
            )


            yield_data = us10y.history(
                period="1d"
            )


            if not yield_data.empty:

                result[
                    "us10y_yield"
                ] = round(
                    float(
                        yield_data["Close"].iloc[-1]
                    ),
                    2
                )



            print(
                "GLOBAL DATA:",
                result
            )


            return result



        except Exception as e:


            print(
                "GLOBAL PROVIDER ERROR:",
                e
            )


            return {

                "xau_usd": None,

                "dxy": None,

                "us10y_yield": None,

                "timestamp": datetime.utcnow()

            }
