from .models import MacroData
from .providers.fred_provider import FredProvider
from app.data.providers import get_best_market_data


class MacroProvider:
    """
    Macro Data Provider Layer

    Aggregates:
    - FRED macro data
    - Market data adapters
    """

    def __init__(self):

        self.fred = FredProvider()


    def fetch(self) -> MacroData:

        fred_data = self.fred.fetch()

        market_data = get_best_market_data()


        dxy = None


        try:

            usd_data = market_data.get(
                "usd_index",
                []
            )


            if isinstance(
                usd_data,
                list
            ) and len(usd_data) > 0:


                dxy = usd_data[0].get(
                    "price"
                )


        except Exception:

            dxy = None



        return MacroData(

            fed_rate=fred_data.get(
                "fed_rate"
            ),

            cpi=fred_data.get(
                "cpi"
            ),

            pce=fred_data.get(
                "pce"
            ),

            nfp=fred_data.get(
                "nfp"
            ),

            dxy=dxy,

            us10y_yield=fred_data.get(
                "us10y_yield"
            ),

            gold_etf_flow=None,

            central_bank_gold_purchase=None,

            timestamp=fred_data.get(
                "timestamp"
            )
        )
