# app/engines/gold/providers/faraz_parser.py

import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Market Parser V6

    Features:
    - Next.js payload extraction
    - Robust row detection
    - Handles escaped JSON
    - Extracts:
        xau_usd
        gold18_price
        mesghal_price
        usd_free_rate
        coin_emami
        coin_bahar
    """


    def parse(self, html: str) -> Dict[str, Any]:

        result: Dict[str, Any] = {}

        try:

            print("######## FARAZ PARSER V6 DEBUG ########")


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


                payload_clean = (
                    payload
                    .replace('\\"', '"')
                    .replace('\\\\', '\\')
                )


                if (
                    "rows" in payload_clean
                    and
                    "lastPrice" in payload_clean
                ):


                    print(
                        "MARKET PAYLOAD FOUND:",
                        index
                    )


                    rows = self.extract_rows(
                        payload_clean
                    )


                    print(
                        "ROWS FOUND:",
                        len(rows)
                    )


                    mapped = self.map_rows(
                        rows
                    )


                    result.update(
                        mapped
                    )


                # XAU extraction

                if "xau" in payload_clean.lower():


                    xau = self.extract_xau(
                        payload_clean
                    )


                    if xau:

                        result["xau_usd"] = xau



            print(
                "FINAL PARSER RESULT:",
                result
            )


            print(
                "####################################"
            )


            return result



        except Exception as e:


            print(
                "FARAZ PARSER ERROR:",
                str(e)
            )


            return {}




    def extract_rows(
        self,
        text: str
    ):


        rows = []


        pattern = re.compile(

            r'"symbol"\s*:\s*"([^"]+)".*?'
            r'"persianName"\s*:\s*"([^"]+)".*?'
            r'"lastPrice"\s*:\s*"([^"]+)"'

        ,
            re.DOTALL

        )


        matches = pattern.findall(
            text
        )



        for item in matches:


            rows.append({

                "symbol":
                    item[0],

                "name":
                    item[1],

                "price":
                    item[2]

            })



        return rows




    def clean_price(
        self,
        value
    ):


        try:


            value = (
                str(value)
                .replace(
                    ",",
                    ""
                )
                .replace(
                    " ",
                    ""
                )
            )


            return float(value)



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


            name = row["name"]


            price = self.clean_price(
                row["price"]
            )



            print(
                "ROW:",
                symbol,
                name,
                price
            )



            if price is None:
                continue



            # طلای ۱۸ عیار

            if (

                "geramtalahejdah" in symbol

                or

                "tala18" in symbol

                or

                "18" in symbol

                or

                "هجده" in name

            ):

                data[
                    "gold18_price"
                ] = price



            # مظنه آبشده

            if (

                "mesghal" in symbol

                or

                "abshode" in symbol

                or

                "مظنه" in name

            ):

                data[
                    "mesghal_price"
                ] = price



            # دلار

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





    def extract_xau(
        self,
        text
    ):


        patterns = [

            r'"xau_usd"\s*:\s*"?([0-9.]+)"?',

            r'xau.{0,80}?([0-9]{3,6}\.?[0-9]*)'

        ]



        for pattern in patterns:


            match = re.search(

                pattern,

                text,

                re.I

            )


            if match:


                try:

                    return float(
                        match.group(1)
                    )

                except:

                    pass



        return None
