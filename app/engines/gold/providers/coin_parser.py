import re
import json
from typing import Dict, Any


class CoinParser:
    """
    Faraz Coin Parser V37

    Extract:
    - coin_emami
    - coin_bahar
    - coin_bubble

    Strategy:
    1- rows extraction
    2- filtered payload search
    3- Persian / English symbols
    4- price fields detection
    """

    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        print("######## COIN PARSER V37 DEBUG ########")
        print("SOURCE:", source)

        result = {}

        try:

            payloads = re.findall(
                r'self\.__next_f\.push\((.*?)\)</script>',
                html,
                re.DOTALL
            )

            print(
                "PAYLOAD COUNT:",
                len(payloads)
            )


            for payload in payloads:

                decoded = (
                    payload
                    .replace('\\"', '"')
                    .replace('\\\\', '\\')
                )


                # حذف بخش های غیر بازار
                if (
                    "blog" in decoded
                    and "lastPrice" not in decoded
                    and "symbol" not in decoded
                ):
                    continue


                rows = self.extract_rows_array(
                    decoded
                )


                if rows:

                    print(
                        "COIN ROWS FOUND:",
                        len(rows)
                    )

                    self.parse_rows(
                        rows,
                        result
                    )


                self.search_payload(
                    decoded,
                    result
                )


            self.calculate_coin_bubble(
                result
            )


            print(
                "FINAL COIN RESULT:",
                result
            )


        except Exception as e:

            print(
                "COIN PARSER ERROR:",
                e
            )


        print(
            "################################"
        )


        return result



    def extract_rows_array(
        self,
        text: str
    ):

        try:

            key = '"rows":'

            start = text.find(
                key
            )

            if start == -1:
                return []


            start = text.find(
                '[',
                start
            )


            if start == -1:
                return []


            depth = 0
            end = None


            for i in range(
                start,
                len(text)
            ):

                if text[i] == '[':
                    depth += 1


                elif text[i] == ']':

                    depth -= 1

                    if depth == 0:

                        end = i + 1
                        break


            if not end:
                return []


            return json.loads(
                text[start:end]
            )


        except Exception as e:

            print(
                "ROWS ERROR:",
                e
            )

            return []



    def parse_rows(
        self,
        rows,
        result
    ):

        for row in rows:

            symbol = str(
                row.get(
                    "symbol",
                    ""
                )
            ).lower()


            name = str(
                row.get(
                    "persianName",
                    ""
                )
            ).lower()


            price = self.clean(
                row.get(
                    "lastPrice"
                )
            )


            print(
                "COIN ROW:",
                symbol,
                name,
                price
            )


            if price is None:
                continue


            if (
                "emami" in symbol
                or "imam" in symbol
                or "sekkeemami" in symbol
                or "امامی" in name
                or "سکه امامی" in name
            ):

                result[
                    "coin_emami"
                ] = price

                print(
                    "EMAMI FOUND ROW:",
                    price
                )


            if (
                "bahar" in symbol
                or "azadi" in symbol
                or "sekebahar" in symbol
                or "بهار" in name
                or "آزادی" in name
            ):

                result[
                    "coin_bahar"
                ] = price

                print(
                    "BAHAR FOUND ROW:",
                    price
                )



    def search_payload(
        self,
        text: str,
        result: Dict
    ):

        patterns = {

            "coin_emami": [

                r'(?:امامی|سکه امامی|emami|imam).{0,500}?(?:lastPrice|price|value)["\':, ]+([0-9,.]+)'

            ],

            "coin_bahar": [

                r'(?:بهار|سکه بهار|bahar|azadi).{0,500}?(?:lastPrice|price|value)["\':, ]+([0-9,.]+)'

            ]

        }


        for key, items in patterns.items():

            if result.get(key):
                continue


            for pattern in items:

                match = re.search(
                    pattern,
                    text,
                    re.IGNORECASE
                )


                if match:

                    value = self.clean(
                        match.group(1)
                    )


                    if value:

                        result[key] = value


                        print(
                            key.upper(),
                            "FOUND PAYLOAD:",
                            value
                        )


                    break



    def calculate_coin_bubble(
        self,
        result: Dict
    ):

        coin = result.get(
            "coin_emami"
        )


        mesghal = result.get(
            "mesghal_price"
        )


        if coin and mesghal:

            try:

                theoretical = mesghal * 0.235


                bubble = (
                    (
                        coin - theoretical
                    )
                    /
                    theoretical
                ) * 100


                result[
                    "coin_bubble"
                ] = round(
                    bubble,
                    2
                )


                print(
                    "COIN BUBBLE:",
                    result["coin_bubble"]
                )


            except Exception as e:

                print(
                    "BUBBLE ERROR:",
                    e
                )



    def clean(
        self,
        value
    ):

        try:

            if value is None:
                return None


            return float(
                str(value)
                .replace(
                    ",",
                    ""
                )
                .replace(
                    "%",
                    ""
                )
            )


        except:

            return None
