import re
import html
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Parser V10

    Extract:
    - mesghal_price
    - gold18_price
    - usd_free_rate
    - coins (future)

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
                "######## FARAZ PARSER V10 DEBUG ########"
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


                if source == "market":

                    if (
                        "rows" in decoded
                        or
                        "lastPrice" in decoded
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
                            self.map_rows(
                                rows
                            )
                        )



                if source == "gold18":

                    price = self.extract_gold18(
                        decoded
                    )


                    if price:

                        result[
                            "gold18_price"
                        ] = price



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
        text
    ):

        rows = []


        symbols = re.finditer(
            r'"symbol"\s*:\s*"([^"]+)"',
            text
        )


        for match in symbols:


            symbol = match.group(1)


            block = text[
                max(
                    0,
                    match.start()-200
                ):
                match.end()+600
            ]



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

                m = re.search(
                    pattern,
                    text
                )

                if m:

                    return m.group(1)


        return None



    def map_rows(
        self,
        rows
    ):

        data = {}

        usd_candidates = []


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

            if symbol in [

                "usdteh-c",

                "usdhrt-c",

                "usdteh-d",

                "usdhrt-d"

            ]:

                usd_candidates.append(
                    (
                        symbol,
                        price
                    )
                )



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



        # انتخاب دلار آزاد

        priority = [

            "usdteh-c",

            "usdhrt-c",

            "usdteh-d",

            "usdhrt-d"

        ]


        for item in priority:

            for symbol, price in usd_candidates:

                if symbol == item:

                    data[
                        "usd_free_rate"
                    ] = price

                    break


            if "usd_free_rate" in data:

                break



        return data



    def extract_gold18(
        self,
        text
    ):


        patterns = [

            r'"lastPrice"\s*:\s*"?(.*?)"?[,}]',

            r'"price"\s*:\s*"?(.*?)"?[,}]',

            r'"value"\s*:\s*"?(.*?)"?[,}]'

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


                if value and value > 100000:

                    return value


        return None



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
                .replace(
                    " ",
                    ""
                )
            )

        except:

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
