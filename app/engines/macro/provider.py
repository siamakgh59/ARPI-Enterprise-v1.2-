from .models import MacroData
from .providers.fred_provider import FredProvider


class MacroProvider:
    """
    Macro Data Provider Layer

    Aggregates macro data sources.
    """

    def __init__(self):
        self.fred = FredProvider()


    def fetch(self) -> MacroData:

        fred_data = self.fred.fetch()


        return MacroData(

            fed_rate=fred_data.get(
                "fed_rate"
            ),

            cpi=fred_data.get(
                "cpi"
            ),

            pce=None,

            nfp=None,

            dxy=None,

            us10y_yield=fred_data.get(
                "us10y_yield"
            ),

            gold_etf_flow=None,

            central_bank_gold_purchase=None,

            timestamp=fred_data.get(
                "timestamp"
            )
        )
