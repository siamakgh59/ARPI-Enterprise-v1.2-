import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz Parser V27 Stable

    استخراج:
    - mesghal_price
    - usd_free_rate
    - gold18_price
    - volume
    - gold_daily_change
    - coin_emami
    - coin_bahar
    """


    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        print("######## FARAZ PARSER V27 DEBUG ########")
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


            for index, payload in enumerate(payloads):


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



            array_text = text[
                start:end
            ]


            return json.loads(
                array_text
            )


        except Exception as e:


            print(
                "ROWS EXTRACT ERROR:",
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



            # مظنه آبشده

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

            if "emami" in symbol:

                result[
                    "coin_emami"
                ] = price



            # سکه بهار

            if "bahar" in symbol:

                result[
                    "coin_bahar"
                ] = price



            if change:

                try:

                    result[
                        "gold_daily_change"
                    ] = float(
                        str(change)
                        .replace(
                            "%",
                            ""
                        )
                        .replace(
                            "+",
                            ""
                        )
                    )

                except:

                    pass





    def extract_gold18(
        self,
        text,
        result
    ):


        try:


            # price

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



            # volume

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



            # change

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


        except Exception as e:

            print(
                "GOLD18 ERROR:",
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
            )


        except:

            return None
