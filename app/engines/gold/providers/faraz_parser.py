# app/engines/gold/providers/faraz_parser.py

import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Parser V7

    Parse:
    - Main gold market page
    - 18K gold detail page

    Output:
    normalized ARPI Gold inputs
    """

    def __init__(self):

        self.result = {}


    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        result = {}

        try:

            print(
                "######## FARAZ PARSER V7 DEBUG ########"
            )

            print(
                "SOURCE:",
                source
            )


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


                if (
                    "rows" in payload
                    or
                    "lastPrice" in payload
                ):

                    print(
                        "MARKET PAYLOAD:",
                        index
                    )


                    rows = self.extract_rows(
                        payload
                    )


                    print(
                        "ROWS FOUND:",
                        len(rows)
                    )


                    result.update(
                        self.map_rows(rows)
                    )



                if source == "gold18":

                    value = self.extract_gold18(
                        payload
                    )

                    if value:

                        result[
                            "gold18_price"
                        ] = value



            print(
                "FINAL RESULT:",
                result
            )


            print(
                "####################################"
            )


            return result



        except Exception as e:


            print(
                "PARSER ERROR:",
                e
            )


            return {}



    def fix_encoding(
        self,
        text: str
    ):

        try:

            if "Ù" in text:

                return (
                    text
                    .encode(
                        "latin1"
                    )
                    .decode(
                        "utf-8"
                    )
                )


        except:

            pass


        return text



    def extract_rows(
        self,
        text
    ):

        rows = []


        pattern = (

            r'"symbol":"(.*?)".*?'
            r'"persianName":"(.*?)".*?'
            r'"lastPrice":("?)([\d\.]+)\3'

        )


        matches = re.findall(
            pattern,
            text,
            re.DOTALL
        )


        for m in matches:


            rows.append({

                "symbol":
                    m[0],

                "name":
                    self.fix_encoding(
                        m[1]
                    ),

                "price":
                    m[3]

            })


        return rows



    def clean(
        self,
        value
    ):


        try:

            return float(
                str(value)
                .replace(
                    ",",
                    ""
                )
            )

        except:

            return None



    def map_rows(
        self,
        rows
    ):

        data = {}


        for row in rows:


            symbol = (
                row["symbol"]
                .lower()
            )


            name = (
                row["name"]
                .lower()
            )


            price = self.clean(
                row["price"]
            )


            print(
                "ROW:",
                symbol,
                name,
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

                data[
                    "mesghal_price"
                ] = price



            # دلار آزاد
            if (

                "usd" in symbol

                or

                "dollar" in symbol

                or

                "دلار" in name

            ):

                data[
                    "usd_free_rate"
                ] = price



            # سکه امامی
            if "emami" in symbol:

                data[
                    "coin_emami"
                ] = price



            # سکه بهار
            if "bahar" in symbol:

                data[
                    "coin_bahar"
                ] = price



        return data



    def extract_gold18(
        self,
        text
    ):

        patterns = [

            r'"lastPrice":"?([0-9\.]+)"?',

            r'"price":"?([0-9\.]+)"?',

            r'"value":"?([0-9\.]+)"?'

        ]


        for pattern in patterns:


            match = re.search(
                pattern,
                text
            )


            if match:

                value = self.clean(
                    match.group(1)
                )


                if value:

                    return value



        return None
