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
                return None


            value = observations[0].get(
                "value"
            )


            if value in (
                None,
                "."
            ):
                return None


            return float(value)


        except Exception:

            return None



    def fetch(self):

        return {

            "fed_rate":
                self.get_series(
                    "FEDFUNDS"
                ),


            "cpi":
                self.get_series(
                    "CPIAUCSL"
                ),


            "pce":
                self.get_series(
                    "PCEPI"
                ),


            "nfp":
                self.get_series(
                    "PAYEMS"
                ),


            "us10y_yield":
                self.get_series(
                    "DGS10"
                ),


            "timestamp":
                datetime.utcnow()

        }
