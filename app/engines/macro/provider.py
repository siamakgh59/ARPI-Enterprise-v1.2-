from .models import MacroData
from datetime import datetime


class MacroProvider:
    """
    Macro Data Provider Layer

    Responsible for collecting and normalizing
    macroeconomic indicators.

    This is the base provider interface.
    Future implementations:
    - FRED Provider
    - Treasury Provider
    - Market Data Provider
    - Gold Flow Provider
    """

    def fetch(self) -> MacroData:
        """
        Fetch latest macro data.

        Current phase:
        Safe placeholder.

        Important:
        Missing data must remain None.
        Never convert missing values to zero.
        """

        return MacroData(
            fed_rate=None,
            cpi=None,
            pce=None,
            nfp=None,
            dxy=None,
            us10y_yield=None,
            gold_etf_flow=None,
            central_bank_gold_purchase=None,
            timestamp=datetime.utcnow()
        )


class LiveMacroProvider(MacroProvider):
    """
    Live Macro Provider.

    Future implementation point for:
    - FRED API
    - US Treasury API
    - Market data feeds
    """

    def fetch(self) -> MacroData:
        """
        Temporary live provider placeholder.

        Will be replaced by real data adapters.
        """

        return super().fetch()
