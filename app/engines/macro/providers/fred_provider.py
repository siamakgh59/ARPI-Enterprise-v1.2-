import os
import requests
from datetime import datetime


class FredProvider:
    """
    FRED Economic Data Provider

    Provides macroeconomic indicators:

    - Federal Funds Rate
    - CPI
    - PCE
    - Non Farm Payroll
    - US 10 Year Treasury Yield
    """


    BASE_URL = (
        "https://api.stlouisfed.org/fred/series/observations"
    )


    def __init__(self):

        self.api_key = os.getenv(
            "FRED_API_KEY"
        )



    def get_series(
        self,
        series_id: str
    ):

        if not self.api_key:

            print(
                "FRED API KEY NOT FOUND"
            )

            return None



        params = {

            "series_id": series_id,

            "api_key": self.api_key,

            "file_type": "json",

            "sort_order": "desc",

            "limit": 1

        }


        try:

            response = requests.get(

                self.BASE_URL,

                params=params,

                timeout=10

            )


            response.raise_for_status()


            data = response.json()


            observations = data.get(

                "observations",

                []

            )


            if not observations:

                print(
                    "NO OBSERVATION:",
                    series_id
                )

                return None



            value = observations[0].get(

                "value"

            )


            if value in (

                None,

                "."

            ):

                print(
                    "INVALID VALUE:",
                    series_id,
                    value
                )

                return None



            return float(value)



        except Exception as e:

            print(

                "FRED ERROR:",

                series_id,

                e

            )

            return None




    def fetch(self):


        fed_rate = self.get_series(
            "FEDFUNDS"
        )


        cpi = self.get_series(
            "CPIAUCSL"
        )


        pce = self.get_series(
            "PCEPI"
        )


        nfp = self.get_series(
            "PAYEMS"
        )


        us10y = self.get_series(
            "DGS10"
        )


        print(
            "DEBUG FRED VALUES:",
            {
                "fed_rate": fed_rate,
                "cpi": cpi,
                "pce": pce,
                "nfp": nfp,
                "us10y_yield": us10y
            }
        )



        return {


            "fed_rate": fed_rate,


            "cpi": cpi,


            "pce": pce,


            "nfp": nfp,


            "us10y_yield": us10y,


            "timestamp": datetime.utcnow()

        }
