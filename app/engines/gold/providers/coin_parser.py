import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz Parser V32

    Extract:
    - mesghal_price
    - usd_free_rate
    - usd_change
    - gold18_price
    - volume
    - gold_daily_change
    - coin_emami
    - coin_bahar
    - coin_bubble
    """


    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        print("######## FARAZ PARSER V32 DEBUG ########")
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


                if source == "market":

                    rows = self.extract_rows_array(
                        decoded
                    )


                    if rows:

                        print(
                            "ROWS FOUND:",
                            len(rows)
                        )

                        self.parse_rows(
                            rows,
                            result
                        )


                    self.extract_coins_from_payload(
                        decoded,
                        result
                    )


                elif source == "gold18":

                    self.extract_gold18(
                        decoded,
                        result
                    )


            if source == "market":

                self.calculate_coin_bubble(
                    result
                )


            print(
                "FINAL RESULT:",
                result
            )


        except Exception as e:

            print(
                "PARSER ERROR:",
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
            )


            price = self.clean(
                row.get(
                    "lastPrice"
                )
            )


            change = self.clean(
                row.get(
                    "changePercent"
                )
            )


            print(
                "ROW:",
                symbol,
                price
            )


            if (
                "abshode" in symbol
                or
                "مظنه" in name
                or
                "آبشده" in name
            ):

                result[
                    "mesghal_price"
                ] = price



            if (
                "harat" in symbol
                or
                "usd" in symbol
                or
                "dollar" in symbol
            ):

                result[
                    "usd_free_rate"
                ] = price


                if change is not None:

                    result[
                        "usd_change"
                    ] = change
                            if (
                "emami" in symbol
                or
                "imam" in symbol
                or
                "sekkeemami" in symbol
                or
                "سکه امامی" in name
            ):

                result[
                    "coin_emami"
                ] = price


                print(
                    "COIN EMAMI FOUND IN ROW:",
                    price
                )



            if (
                "bahar" in symbol
                or
                "azadi" in symbol
                or
                "sekebahar" in symbol
                or
                "بهار" in name
            ):

                result[
                    "coin_bahar"
                ] = price


                print(
                    "COIN BAHAR FOUND IN ROW:",
                    price
                )



            if change is not None:

                result[
                    "gold_daily_change"
                ] = change




    def extract_coins_from_payload(
        self,
        text: str,
        result: Dict
    ):

        try:

            if result.get(
                "coin_emami"
            ) is None:

                patterns = [

                    r'سکه امامی.{0,300}?lastPrice["\': ]+([0-9,.]+)',

                    r'emami.{0,300}?lastPrice["\': ]+([0-9,.]+)',

                    r'imam.{0,300}?lastPrice["\': ]+([0-9,.]+)'

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

                    r'سکه بهار.{0,300}?lastPrice["\': ]+([0-9,.]+)',

                    r'bahar.{0,300}?lastPrice["\': ]+([0-9,.]+)',

                    r'azadi.{0,300}?lastPrice["\': ]+([0-9,.]+)'

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
                "COIN EXTRACTION ERROR:",
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



    def extract_gold18(
        self,
        text,
        result
    ):

        prices = re.findall(
            r'"price":(\d+)',
            text
        )


        if prices:

            result[
                "gold18_price"
            ] = float(
                prices[-1]
            )



        volumes = re.findall(
            r'"volume":(\d+)',
            text
        )


        if volumes:

            result[
                "volume"
            ] = float(
                volumes[-1]
            )



        changes = re.findall(
            r'"changePercent":(-?\d+\.?\d*)',
            text
        )


        if changes:

            result[
                "gold_daily_change"
            ] = float(
                changes[-1]
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
