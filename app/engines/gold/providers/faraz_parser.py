import re
import json
import html
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Parser V9

    Robust Next.js payload parser

    Sources:
    - market
    - gold18
    """

    def parse(
        self,
        html_source: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        result = {}

        try:

            print(
                "######## FARAZ PARSER V9 DEBUG ########"
            )

            print(
                "SOURCE:",
                source
            )


            payloads = re.findall(
                r'self\.__next_f\.push\((.*?)\)',
                html_source,
                re.DOTALL
            )


            print(
                "PAYLOAD COUNT:",
                len(payloads)
            )


            for index, payload in enumerate(payloads):

                decoded = self.decode_payload(
                    payload
                )


                if index == 0:

                    print(
                        "DECODE SAMPLE:",
                        decoded[:300]
                    )



                if source == "market":

                    if (
                        "lastPrice" in decoded
                        or
                        "rows" in decoded
                    ):

                        print(
                            "MARKET PAYLOAD:",
                            index
                        )


                        rows = self.extract_rows(
                            decoded
                        )


                        print(
                            "ROWS FOUND:",
                            len(rows)
                        )


                        result.update(
                            self.map_rows(rows)
                        )



                if source == "gold18":

                    value = self.extract_price(
                        decoded
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



    def decode_payload(
        self,
        text: str
    ) -> str:


        try:

            text = (
                text
                .encode(
                    "utf-8"
                )
                .decode(
                    "unicode_escape"
                )
            )


        except:

            pass


        try:

            text = html.unescape(
                text
            )


        except:

            pass


        return text



    def extract_rows(
        self,
        text: str
    ):


        rows = []


        # استخراج هر symbol

        symbols = re.finditer(
            r'"symbol"\s*:\s*"([^"]+)"',
            text
        )


        for symbol_match in symbols:


            symbol = symbol_match.group(1)


            start = max(
                0,
                symbol_match.start()-200
            )


            end = (
                symbol_match.end()+500
            )


            block = text[start:end]



            name = self.find_value(
                block,
                [
                    "persianName",
                    "name",
                    "title"
                ]
            )


            price = self.find_value(
                block,
                [
                    "lastPrice",
                    "price",
                    "value"
                ]
            )



            if price:


                rows.append({

                    "symbol":
                        symbol,

                    "name":
                        self.fix_encoding(
                            name or ""
                        ),

                    "price":
                        price

                })



        return rows



    def find_value(
        self,
        text,
        keys
    ):


        for key in keys:


            patterns = [

                rf'"{key}"\s*:\s*"([^"]+)"',

                rf'"{key}"\s*:\s*([0-9\.]+)'

            ]


            for pattern in patterns:


                match = re.search(
                    pattern,
                    text
                )


                if match:

                    return match.group(1)



        return None



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
                .replace(",","")
                .replace(" ","")
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



            if not price:

                continue



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



            if "emami" in symbol:

                data[
                    "coin_emami"
                ] = price



            if "bahar" in symbol:

                data[
                    "coin_bahar"
                ] = price



        return data



    def extract_price(
        self,
        text
    ):


        values = re.findall(

            r'"(?:lastPrice|price|value)"\s*:\s*"?([0-9\.]+)"?',

            text

        )


        for value in values:


            number = self.clean(
                value
            )


            if number and number > 100000:

                return number



        return None
