import re
import json
from typing import Dict, Any


class CoinParser:
    """
    Faraz Coin Parser V35

    Extract:
    - coin_emami
    - coin_bahar
    - coin_bubble

    Supports:
    - Next.js self.__next_f payload
    - rows
    - Persian names
    - English symbols
    - payload debug
    """

    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        print("######## COIN PARSER V35 DEBUG ########")
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


                self.extract_from_payload(
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
                "[",
                start
            )

            if start == -1:
                return []


            depth = 0


            for i in range(
                start,
                len(text)
            ):

                if text[i] == "[":
                    depth += 1


                elif text[i] == "]":

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


            if price is None:
                continue



            if (
                "emami" in symbol
                or
                "imam" in symbol
                or
                "sekke" in symbol
                or
                "امامی" in name
                or
                ("سکه" in name and "امام" in name)
            ):

                result[
                    "coin_emami"
                ] = price

                print(
                    "COIN EMAMI FOUND:",
                    price
                )



            if (
                "bahar" in symbol
                or
                "azadi" in symbol
                or
                "بهار" in name
                or
                "آزادی" in name
            ):

                result[
                    "coin_bahar"
                ] = price

                print(
                    "COIN BAHAR FOUND:",
                    price
                )



    def extract_from_payload(
        self,
        text: str,
        result: Dict
    ):

        try:

            if "سکه" in text:

                index = text.find(
                    "سکه"
                )

                print(
                    "######## COIN CONTEXT ########"
                )

                print(
                    text[index:index+800]
                )

                print(
                    "##############################"
                )



            if result.get(
                "coin_emami"
            ) is None:


                patterns = [

                    r'سکه.{0,500}?امامی.{0,500}?(?:lastPrice|price|value).{0,50}?([0-9,.]+)',

                    r'امامی.{0,500}?(?:lastPrice|price|value).{0,50}?([0-9,.]+)',

                    r'emami.{0,500}?(?:lastPrice|price|value).{0,50}?([0-9,.]+)',

                    r'imam.{0,500}?(?:lastPrice|price|value).{0,50}?([0-9,.]+)'

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
                            "EMAMI PAYLOAD FOUND:",
                            result["coin_emami"]
                        )

                        break



            if result.get(
                "coin_bahar"
            ) is None:


                patterns = [

                    r'سکه.{0,500}?بهار.{0,500}?(?:lastPrice|price|value).{0,50}?([0-9,.]+)',

                    r'بهار.{0,500}?(?:lastPrice|price|value).{0,50}?([0-9,.]+)',

                    r'bahar.{0,500}?(?:lastPrice|price|value).{0,50}?([0-9,.]+)',

                    r'azadi.{0,500}?(?:lastPrice|price|value).{0,50}?([0-9,.]+)'

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
                            "BAHAR PAYLOAD FOUND:",
                            result["coin_bahar"]
                        )

                        break



        except Exception as e:

            print(
                "PAYLOAD ERROR:",
                e
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

                theoretical = (
                    mesghal *
                    0.235
                )


                result[
                    "coin_bubble"
                ] = round(
                    (
                        (coin - theoretical)
                        /
                        theoretical
                    ) * 100,
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
