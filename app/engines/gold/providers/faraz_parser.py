import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Market Parser v3

    Purpose:
    - Parse Next.js streamed payload
    - Decode escaped payloads
    - Extract Iranian gold/currency market data

    Output:
    GoldNormalizer compatible dictionary
    """

    def parse(
        self,
        html: str
    ) -> Dict[str, Any]:

        result = {}

        try:

            payloads = re.findall(
                r'self\.__next_f\.push\((.*?)\)</script>',
                html,
                re.DOTALL
            )

            print("######## FARAZ PARSER DEBUG ########")
            print(
                "PAYLOAD COUNT:",
                len(payloads)
            )


            decoded_payloads = []


            for index, payload in enumerate(payloads):

                try:

                    decoded = payload.encode(
                        "utf-8"
                    ).decode(
                        "unicode_escape"
                    )

                except:

                    decoded = payload


                decoded_payloads.append(
                    decoded
                )


                keys = []

                for key in [
                    "rows",
                    "lastPrice",
                    "gold",
                    "usd",
                    "emami",
                    "bahar",
                    "mesghal"
                ]:

                    if key.lower() in decoded.lower():

                        keys.append(key)


                if keys:

                    print(
                        f"PAYLOAD {index} KEYS:",
                        keys
                    )


            #
            # Extract market rows
            #

            for payload in decoded_payloads:


                if (
                    "lastPrice" in payload
                    and "symbol" in payload
                ):


                    rows = self.extract_rows(
                        payload
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



            #
            # Extract global gold ounce
            #

            for payload in decoded_payloads:


                if "xau" in payload.lower():


                    xau = self.extract_xau(
                        payload
                    )


                    if xau:

                        result[
                            "xau_usd"
                        ] = xau



            print(
                "PARSER RESULT:",
                result
            )

            print(
                "####################################"
            )


            return result



        except Exception as e:


            print(
                "Faraz Parser Error:",
                str(e)
            )

            return {}



    def extract_rows(
        self,
        text: str
    ):

        rows = []


        pattern = (

            r'"symbol"\s*:\s*"([^"]+)".*?'
            r'"persianName"\s*:\s*"([^"]+)".*?'
            r'"lastPrice"\s*:\s*"([^"]+)"'

        )


        matches = re.findall(
            pattern,
            text,
            re.DOTALL
        )


        for match in matches:


            rows.append(

                {

                    "symbol": match[0],

                    "name": match[1],

                    "price": match[2]

                }

            )


        return rows



    def clean_number(
        self,
        value
    ):

        try:

            value = (
                value
                .replace(
                    ",",
                    ""
                )
                .replace(
                    " ",
                    ""
                )
            )


            return float(
                value
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


            name = row["name"]


            price = self.clean_number(
                row["price"]
            )


            print(
                "ROW:",
                symbol,
                name,
                price
            )



            #
            # Gold 18
            #

            if (
                "18" in symbol
                or
                "geram18" in symbol
                or
                "طلا ۱۸" in name
                or
                "طلای ۱۸" in name
            ):

                data[
                    "gold18_price"
                ] = price



            #
            # Mesghal
            #

            if (
                "mesghal" in symbol
                or
                "abshode" in symbol
                or
                "مظنه" in name
                or
                "مثقال" in name
            ):

                data[
                    "mesghal_price"
                ] = price



            #
            # USD Iran
            #

            if (
                "usd" in symbol
                or
                "dollar" in symbol
                or
                "دلار" in name
                or
                "تتر" in name
            ):

                data[
                    "usd_free_rate"
                ] = price



            #
            # Coins
            #

            if (
                "emami" in symbol
                or
                "امامی" in name
            ):

                data[
                    "coin_emami"
                ] = price



            if (
                "bahar" in symbol
                or
                "بهار" in name
            ):

                data[
                    "coin_bahar"
                ] = price



        return data



    def extract_xau(
        self,
        text
    ):

        patterns = [

            r'"xau_usd".*?([0-9]{3,6})',

            r'"xau".*?([0-9]{3,6})',

            r'ounce.*?([0-9]{3,6})'

        ]


        for pattern in patterns:


            match = re.search(
                pattern,
                text,
                re.I | re.DOTALL
            )


            if match:


                try:

                    return float(
                        match.group(1)
                    )

                except:

                    pass


        return None
