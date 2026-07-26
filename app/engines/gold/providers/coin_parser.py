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

    Supports:
    - rows extraction
    - full payload scanning
    - Persian names
    - English symbols
    - Next.js stream data
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


                self.extract_payload_coins(
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


            if self.is_emami(
                symbol,
                name
            ):

                result[
                    "coin_emami"
                ] = price

                print(
                    "COIN EMAMI FOUND ROW:",
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
                    "COIN BAHAR FOUND ROW:",
                    price
                )



    def extract_payload_coins(
        self,
        text: str,
        result: Dict
    ):

        try:

            keywords = [
                "سکه",
                "امامی",
                "بهار",
                "azadi",
                "emami",
                "imam",
                "bahar",
                "sekke"
            ]


            for key in keywords:

                index = text.lower().find(
                    key.lower()
                )

                if index != -1:

                    context = text[
                        max(0,index-150):
                        index+300
                    ]

                    print(
                        "######## COIN CONTEXT ########"
                    )

                    print(
                        context
                    )

                    print(
                        "##############################"
                    )

                    break



            if result.get(
                "coin_emami"
            ) is None:


                patterns = [

                    r'(?:امامی|emami|imam|sekkeemami).{0,500}?(?:lastPrice|price)["\':, ]+([0-9,.]+)',

                    r'(?:lastPrice|price)["\':, ]+([0-9,.]+).{0,200}?(?:امامی|emami)'

                ]


                for pattern in patterns:

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


                patterns = [

                    r'(?:بهار|bahar|azadi|sekebahar).{0,500}?(?:lastPrice|price)["\':, ]+([0-9,.]+)',

                    r'(?:lastPrice|price)["\':, ]+([0-9,.]+).{0,200}?(?:بهار|bahar|azadi)'

                ]


                for pattern in patterns:

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


        except Exception as e:

            print(
                "PAYLOAD EXTRACTION ERROR:",
                e
            )



    def is_emami(
        self,
        symbol,
        name
    ):

        return (
            "emami" in symbol
            or "imam" in symbol
            or "sekkeemami" in symbol
            or "امامی" in name
            or "سکه امامی" in name
        )



    def is_bahar(
        self,
        symbol,
        name
    ):

        return (
            "bahar" in symbol
            or "azadi" in symbol
            or "sekebahar" in symbol
            or "بهار" in name
            or "آزادی" in name
        )



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
