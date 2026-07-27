from typing import Optional


class CoinBubbleCalculator:
    """
    ARPI Coin Bubble Calculator v1.0

    Responsible for:
    - Coin intrinsic value estimation
    - Bubble percentage calculation
    - Separation from scoring engine
    """

    VERSION = "1.0.0"


    def calculate(
        self,
        coin_price: Optional[float],
        mesghal_price: Optional[float]
    ) -> Optional[float]:

        if not coin_price or not mesghal_price:
            return None


        try:

            # Gold content assumptions
            #
            # Imam coin:
            # 8.133 grams total weight
            # 91.6% purity

            gold_ratio = (
                8.133
                /
                4.3318
            )


            theoretical_price = (
                mesghal_price
                *
                gold_ratio
                *
                0.916
            )


            bubble = (
                (
                    coin_price
                    -
                    theoretical_price
                )
                /
                theoretical_price
            ) * 100


            return round(
                bubble,
                2
            )


        except Exception as e:

            print(
                "COIN BUBBLE CALCULATOR ERROR:",
                e
            )

            return None
