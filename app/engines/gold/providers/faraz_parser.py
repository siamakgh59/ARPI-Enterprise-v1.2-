import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz Parser V28

    Extract:
    - mesghal_price
    - usd_free_rate
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

        print("######## FARAZ PARSER V28 DEBUG ########")
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


                elif source == "gold18":

                    self.extract_gold18(
                        decoded,
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

            start = text.find(key)

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


            change = row.get(
                "changePercent"
            )


            print(
                "ROW:",
                symbol,
                price
            )



            # مظنه

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



            # دلار

            if (
                "harat" in symbol
                or
                "usd" in symbol
            ):

                result[
                    "usd_free_rate"
                ] = price



            # سکه امامی

            if (
                "emami" in symbol
                or
                "imam" in symbol
                or
                "امامی" in name
            ):

                result[
                    "coin_emami"
                ] = price



            # سکه بهار آزادی

            if (
                "bahar" in symbol
                or
                "azadi" in symbol
                or
                "بهار" in name
            ):

                result[
                    "coin_bahar"
                ] = price



            if change:

                try:

                    result[
                        "gold_daily_change"
                    ] = float(
                        str(change)
                        .replace("%","")
                        .replace("+","")
                    )

                except:

                    pass



        # محاسبه حباب سکه

        self.calculate_coin_bubble(
            result
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


            except:

                pass



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
            )


        except:

            return None
