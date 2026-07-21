from .models import MacroData


class MacroProvider:
    """
    Macro Data Provider Layer
    Responsible for collecting macro indicators.
    """

    def fetch(self) -> MacroData:

        return MacroData(

            fed_rate=None,
            cpi=None,
            pce=None,
            nfp=None,
            dxy=None,
            us10y_yield=None,
            gold_etf_flow=None,
            central_bank_gold_purchase=None
        )
