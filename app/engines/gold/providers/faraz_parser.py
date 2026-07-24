import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Parser V14 Stable

    Responsibilities:

    - Parse Next.js payloads
    - Extract market rows
    - Extract 18K gold price
    - Normalize Faraz data for ARPI Gold Engine

    Supported outputs:

    mesghal_price
    gold18_price
    usd_free_rate
    coin_emami
    coin_bahar
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
                "######## FARAZ PARSER V14 DEBUG ########"
            )

            print(
                "SOURCE:",
                source
            )


            payloads = self.extract_payloads(
                html
            )


            print(
                "PAYLOAD COUNT:",
                len(payloads)
            )


            for index, payload in enumerate(payloads):

                decoded = self.decode_payload(
                    payload
                )


                if source == "market":


                    if (
                        "rows" in decoded
                        or
                        "lastPrice" in decoded
                    ):


                        rows = self.extract_rows(
                            decoded
                        )


                        print(
                            "MARKET PAYLOAD:",
                            index
                        )


                        print(
                            "ROWS FOUND:",
                            len(rows)
                        )


                        market_data = self.map_rows(
                            rows
                        )


                        result.update(
                            market_data
                        )



                if source == "gold18":


                    gold18 = self.extract_gold18(
                        decoded
                    )


                    if gold18:


                        result[
                            "gold18_price"
                        ] = gold18



            result = self.validate_result(
                result
            )


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
                str(e)
            )


            return {}



    def extract_payloads(
        self,
        html: str
    ):

        return re.findall(

            r'self\.__next_f\.push\((.*?)\)</script>',

            html,

            re.DOTALL

        )



    def decode_payload(
        self,
        payload: str
    ):

        """
        Decode Next.js escaped payload
        """

        try:

            payload = (
                payload
                .encode()
                .decode(
                    "unicode_escape"
                )
            )


        except:

            pass


        return payload



    def extract_rows(
        self,
        text: str
    ):


        rows = []


        pattern = (

            r'"symbol"\s*:\s*"([^"]+)".*?'

            r'"persianName"\s*:\s*"([^"]+)".*?'

            r'"lastPrice"\s*:\s*"?([\d\.]+)"?'

        )


        matches = re.findall(

            pattern,

            text,

            re.DOTALL

        )



        for symbol, name, price in matches:


            rows.append({

                "symbol":
                    symbol,

                "name":
                    self.fix_encoding(
                        name
                    ),

                "price":
                    price

            })


        return rows



    def fix_encoding(
        self,
        text
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



            # مظنه آبشده جهانی

            if (

                "abshode" in symbol
                or
                "mesghal" in symbol
                or
                "مظنه" in name
                or
                "آبشده" in name

            ):


                if price and price > 1000000:

                    data[
                        "mesghal_price"
                    ] = price



            # دلار

            elif (

                "usd" in symbol
                or
                "dollar" in symbol
                or
                "دلار" in name

            ):


                if price and price > 10000:

                    data[
                        "usd_free_rate"
                    ] = price



            # سکه امامی

            elif "emami" in symbol:


                data[
                    "coin_emami"
                ] = price



            # سکه بهار

            elif "bahar" in symbol:


                data[
                    "coin_bahar"
                ] = price



        return data



    def extract_gold18(
        self,
        text
    ):


        patterns = [


            r'"lastPrice"\s*:\s*"?([0-9\.]+)"?',


            r'"price"\s*:\s*"?([0-9\.]+)"?',


            r'"value"\s*:\s*"?([0-9\.]+)"?',


            r'"amount"\s*:\s*"?([0-9\.]+)"?'


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


                if (

                    value
                    and
                    value > 1000000

                ):

                    return value



        return None



    def validate_result(
        self,
        data
    ):


        validated = {}



        for key, value in data.items():


            if value is None:

                continue



            if key == "mesghal_price":

                if value > 1000000:

                    validated[key] = value



            elif key == "gold18_price":

                if value > 1000000:

                    validated[key] = value



            elif key == "usd_free_rate":

                if value > 10000:

                    validated[key] = value



            else:

                validated[key] = value



        return validated
