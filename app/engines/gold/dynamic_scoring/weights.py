"""
ARPI Gold Dynamic Weight Engine v1.0

Centralized scoring weights.

Future:
- Regime adjustment
- Market cycle adaptation
- AI optimization
"""


class GoldDynamicWeights:


    VERSION = "1.0.0"



    BASE_WEIGHTS = {


        # Domestic Gold Market

        "gold18_price": 0.15,

        "mesghal_price": 0.10,


        # Currency Effect

        "usd_free_rate": 0.20,

        "usd_change": 0.05,


        # Global Market

        "xau_usd": 0.20,

        "dxy": 0.10,

        "us10y_yield": 0.10,


        # Market Behavior

        "gold_momentum": 0.05,

        "volume": 0.02,


        # Risk

        "coin_bubble": 0.03

    }



    def get_weights(self):

        """
        Return active weights.

        Later:
        This method will receive
        market regime and modify weights.
        """

        return self.BASE_WEIGHTS.copy()
