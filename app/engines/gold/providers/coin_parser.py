import re


class CoinParser:
    """
    ARPI Coin Parser v1.0
    """


    def parse(
        self,
        html: str
    ):

        result = {}


        try:

            prices = re.findall(
                r'"price":(\d+)',
                html
            )


            if prices:

                result[
                    "coin_price"
                ] = float(
                    prices[-1]
                )


        except Exception as e:

            print(
                "COIN PARSER ERROR:",
                e
            )


        return result
