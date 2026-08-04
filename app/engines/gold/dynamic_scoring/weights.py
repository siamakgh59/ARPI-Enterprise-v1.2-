"""
ARPI Gold Dynamic Weight Engine v1.0

Centralized scoring weights.

Future:
- Market regime adjustment
- AI optimization
- Historical calibration
"""


class GoldDynamicWeights:


    VERSION = "1.0.0"



    BASE_WEIGHTS = {


        # Domestic Market

        "gold18_price": 0.15,

        "mesghal_price": 0.10,


        # Currency

        "usd_free_rate": 0.20,

        "usd_change": 0.05,


        # Global Market

        "xau_usd": 0.20,

        "dxy": 0.10,

        "us10y_yield": 0.10,


        # Momentum

        "gold_momentum": 0.05,


        # Liquidity

        "volume": 0.02,


        # Risk

        "coin_bubble": 0.03

    }



    def get_weights(self):

        """
        Return active weights.

        Later versions:
        - regime based weights
        - adaptive weights
        """

        return self.BASE_WEIGHTS.copy()
