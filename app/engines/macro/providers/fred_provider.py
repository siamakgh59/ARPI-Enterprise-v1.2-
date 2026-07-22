import os
import time
import requests
from datetime import datetime


class FredProvider:
    """
    FRED Economic Data Provider

    ARPI Macro Reliability Layer v1.1

    Features:
    - Retry mechanism
    - Timeout handling

    Provides:
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

        self.max_retries = 3



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



        for attempt in range(
            1,
            self.max_retries + 1
        ):

            try:

                print(
                    f"FRED REQUEST {series_id} ATTEMPT {attempt}"
                )


                response = requests.get(

                    self.BASE_URL,

                    params=params,

                    timeout=15

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



            except requests.exceptions.Timeout:

                print(
                    f"FRED TIMEOUT {series_id} ATTEMPT {attempt}"
                )



            except Exception as e:

                print(
                    "FRED ERROR:",
                    series_id,
                    e
                )



            if attempt < self.max_retries:

                wait_time = attempt * 2

                print(
                    f"RETRY WAIT {wait_time}s"
                )

                time.sleep(
                    wait_time
                )



        print(
            "FRED FAILED AFTER RETRIES:",
            series_id
        )


        return None




    def fetch(self):

        print(
            "######## FRED PROVIDER FETCH ACTIVE ########"
        )


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


        us10y_yield = self.get_series(
            "DGS10"
        )



        print(
            "######## FRED VALUES ########"
        )


        print(
            {
                "fed_rate": fed_rate,
                "cpi": cpi,
                "pce": pce,
                "nfp": nfp,
                "us10y_yield": us10y_yield
            }
        )


        print(
            "#############################"
        )



        return {

            "fed_rate": fed_rate,

            "cpi": cpi,

            "pce": pce,

            "nfp": nfp,

            "us10y_yield": us10y_yield,

            "timestamp": datetime.utcnow()

        }
