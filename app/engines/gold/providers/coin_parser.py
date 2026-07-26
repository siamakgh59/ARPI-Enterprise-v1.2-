import re
import json
from typing import Dict, Any


class CoinParser:
    """
    Faraz Coin Parser V38

    Extract:
    - coin_emami
    - coin_bahar
    - coin_bubble
    """

    def parse(
        self,
        html: str,
        source: str = "coin"
    ) -> Dict[str, Any]:

        print("######## COIN PARSER V38 DEBUG ########")
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
        text
    ):

        try:

            index = text.find(
                '"rows":'
            )

            if index == -1:
                return []


            start = text.find(
                '[',
                index
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


            if self.is_emami(
                symbol,
                name
            ):

                result[
                    "coin_emami"
                ] = price

                print(
                    "COIN EMAMI FOUND:",
                    price
                )


            if self.is_bahar(
                symbol,
                name
            ):

                result[
                    "coin_bahar"
                ] = price

                print(
                    "COIN BAHAR FOUND:",
                    price
                )



    def search_payload(
        self,
        text,
        result
    ):


        if result.get(
            "coin_emami"
        ) is None:


            patterns = [

                r'(?:سکه\s*امامی|امامی).*?(?:lastPrice|price).*?([0-9]{5,})',

                r'(?:emami|imam).*?(?:lastPrice|price).*?([0-9]{5,})',

            ]


            for p in patterns:

                match = re.search(
                    p,
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
                        "PAYLOAD EMAMI FOUND:",
                        result["coin_emami"]
                    )

                    break



        if result.get(
            "coin_bahar"
        ) is None:


            patterns = [

                r'(?:سکه\s*بهار|بهار\s*آزادی).*?(?:lastPrice|price).*?([0-9]{5,})',

                r'(?:bahar|azadi).*?(?:lastPrice|price).*?([0-9]{5,})',

            ]


            for p in patterns:

                match = re.search(
                    p,
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
                        "PAYLOAD BAHAR FOUND:",
                        result["coin_bahar"]
                    )

                    break



    def is_emami(
        self,
        symbol,
        name
    ):

        keys = [
            "emami",
            "imam",
            "sekkeemami",
            "سکه امامی",
            "امامی"
        ]

        return any(
            x in symbol or x in name
            for x in keys
        )



    def is_bahar(
        self,
        symbol,
        name
    ):

        keys = [
            "bahar",
            "azadi",
            "sekebahar",
            "سکه بهار",
            "بهار",
            "آزادی"
        ]

        return any(
            x in symbol or x in name
            for x in keys
        )



    def calculate_coin_bubble(
        self,
        result
    ):

        coin = result.get(
            "coin_emami"
        )

        mesghal = result.get(
            "mesghal_price"
        )


        if coin and mesghal:

            theoretical = (
                mesghal * 0.235
            )


            result[
                "coin_bubble"
            ] = round(
                (
                    (
                        coin -
                        theoretical
                    )
                    /
                    theoretical
                ) * 100,
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
