class CoinBubbleCalculator:
    """
    ARPI Coin Bubble Calculator v1.0
    """

    VERSION = "1.0.0"


    def calculate(
        self,
        coin_price,
        mesghal_price
    ):

        if not coin_price or not mesghal_price:
            return None


        # تبدیل تقریبی:
        # هر مثقال = 4.3318 گرم
        # سکه امامی = 8.133 گرم طلای خالص

        theoretical_coin = (
            mesghal_price
            *
            (8.133 / 4.3318)
            *
            0.916
        )


        bubble = (
            (
                coin_price
                -
                theoretical_coin
            )
            /
            theoretical_coin
        ) * 100


        return round(
            bubble,
            2
        )
