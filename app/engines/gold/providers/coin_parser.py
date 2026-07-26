import re
import json
from typing import Dict, Any


class CoinParser:
    """
    Faraz Coin Parser V36

    Extract:
    - coin_emami
    - coin_bahar
    - coin_bubble

    Sources:
    - rows array
    - next_f payload
    - Persian names
    - English symbols
    """

    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        print("######## COIN PARSER V36 DEBUG ########")
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


                if "سکه" in decoded or "coin" in decoded.lower():

                    print(
                        "######## COIN CONTEXT ########"
                    )

                    index = decoded.find("سکه")

                    if index != -1:

                        print(
                            decoded[index:index+500]
                        )


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


                self.extract_payload(
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

            for i in range(
                start,
                len(text)
            ):

                if text[i] == '[':

                    depth += 1


                elif text[i] == ']':

                    depth -= 1


                    if depth == 0:

                        return json.loads(
                            text[start:i+1]
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
        result: Dict
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



            if (
                "emami" in symbol
                or
                "imam" in symbol
                or
                "sekkeemami" in symbol
                or
                "سکه امامی" in name
                or
                "امامی" in name
            ):

                result[
                    "coin_emami"
                ] = price


                print(
                    "COIN EMAMI FOUND ROW:",
                    price
                )



            if (
                "bahar" in symbol
                or
                "azadi" in symbol
                or
                "sekebahar" in symbol
                or
                "سکه بهار" in name
                or
                "بهار" in name
            ):

                result[
                    "coin_bahar"
                ] = price


                print(
                    "COIN BAHAR FOUND ROW:",
                    price
                )



    def extract_payload(
        self,
        text: str,
        result: Dict
    ):


        patterns_emami = [

            r'سکه.{0,100}?امامی.{0,300}?(?:lastPrice|price)["\':, ]+([0-9,.]+)',

            r'emami.{0,300}?(?:lastPrice|price)["\':, ]+([0-9,.]+)',

            r'imam.{0,300}?(?:lastPrice|price)["\':, ]+([0-9,.]+)'

        ]


        patterns_bahar = [

            r'سکه.{0,100}?بهار.{0,300}?(?:lastPrice|price)["\':, ]+([0-9,.]+)',

            r'bahar.{0,300}?(?:lastPrice|price)["\':, ]+([0-9,.]+)',

            r'azadi.{0,300}?(?:lastPrice|price)["\':, ]+([0-9,.]+)'

        ]



        if result.get(
            "coin_emami"
        ) is None:


            for pattern in patterns_emami:

                match = re.search(
                    pattern,
                    text,
                    re.IGNORECASE
                )


                if match:

                    result[
                        "coin_emami"
                    ] = self.clean(
                        match.group(1)
                    )


                    print(
                        "COIN EMAMI FOUND PAYLOAD:",
                        result["coin_emami"]
                    )

                    break



        if result.get(
            "coin_bahar"
        ) is None:


            for pattern in patterns_bahar:

                match = re.search(
                    pattern,
                    text,
                    re.IGNORECASE
                )


                if match:

                    result[
                        "coin_bahar"
                    ] = self.clean(
                        match.group(1)
                    )


                    print(
                        "COIN BAHAR FOUND PAYLOAD:",
                        result["coin_bahar"]
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

            theoretical = mesghal * 0.235


            bubble = (
                (coin - theoretical)
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
