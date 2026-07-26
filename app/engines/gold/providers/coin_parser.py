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

    Supports:
    - rows extraction
    - full payload search
    - Persian names
    - English symbols
    - Next.js payload
    """

    def parse(
        self,
        html: str,
        source: str = "market"
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


                self.extract_coin_payload(
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



            if any(
                x in symbol
                for x in [
                    "emami",
                    "imam",
                    "sekkeemami",
                    "coinemami"
                ]
            ) or any(
                x in name
                for x in [
                    "امامی",
                    "سکه امامی"
                ]
            ):

                result[
                    "coin_emami"
                ] = price


                print(
                    "COIN EMAMI FOUND:",
                    price
                )



            if any(
                x in symbol
                for x in [
                    "bahar",
                    "azadi",
                    "sekebahar"
                ]
            ) or any(
                x in name
                for x in [
                    "بهار",
                    "آزادی"
                ]
            ):

                result[
                    "coin_bahar"
                ] = price


                print(
                    "COIN BAHAR FOUND:",
                    price
                )



    def extract_coin_payload(
        self,
        text: str,
        result: Dict
    ):


        patterns_emami = [

            r'(?:سکه\s*امامی|امامی|emami|imam).*?(?:lastPrice|price).*?([0-9]{5,})',

            r'(?:lastPrice|price).*?([0-9]{5,}).{0,150}?(?:emami|imam)',

        ]


        patterns_bahar = [

            r'(?:سکه\s*بهار|بهار\s*آزادی|bahar|azadi).*?(?:lastPrice|price).*?([0-9]{5,})',

            r'(?:lastPrice|price).*?([0-9]{5,}).{0,150}?(?:bahar|azadi)',

        ]


        if result.get(
            "coin_emami"
        ) is None:


            for p in patterns_emami:

                m = re.search(
                    p,
                    text,
                    re.IGNORECASE
                )

                if m:

                    result[
                        "coin_emami"
                    ] = self.clean(
                        m.group(1)
                    )

                    print(
                        "PAYLOAD EMAMI FOUND:",
                        result["coin_emami"]
                    )

                    break



        if result.get(
            "coin_bahar"
        ) is None:


            for p in patterns_bahar:

                m = re.search(
                    p,
                    text,
                    re.IGNORECASE
                )

                if m:

                    result[
                        "coin_bahar"
                    ] = self.clean(
                        m.group(1)
                    )

                    print(
                        "PAYLOAD BAHAR FOUND:",
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

            try:

                theoretical = (
                    mesghal *
                    0.235
                )


                bubble = (
                    (
                        coin -
                        theoretical
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
