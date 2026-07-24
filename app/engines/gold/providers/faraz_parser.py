import re
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Parser V15 Stable

    Features:

    - Parse Faraz Next.js payloads
    - Extract market rows
    - Extract 18K gold price
    - Unit normalization
    - Handle compressed prices:
        42   -> 42,000,000
        192  -> 192,000

    Output:

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
                "######## FARAZ PARSER V15 DEBUG ########"
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


                payload = self.decode_payload(
                    payload
                )


                if source == "market":


                    if (
                        "rows" in payload
                        or
                        "lastPrice" in payload
                    ):


                        rows = self.extract_rows(
                            payload
                        )


                        print(
                            "MARKET PAYLOAD:",
                            index
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


        try:

            return (
                payload
                .encode()
                .decode(
                    "unicode_escape"
                )
            )

        except:

            return payload



    def extract_rows(
        self,
        text: str
    ):


        rows = []


        pattern = (

            r'"symbol"\s*:\s*"([^"]+)".*?'

            r'"persianName"\s*:\s*"([^"]+)".*?'

            r'"lastPrice"\s*:\s*"?([0-9\.]+)"?'

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



    def normalize_price(
        self,
        value,
        price_type
    ):


        """
        Faraz sometimes returns compressed values.

        Example:

        mesghal:
        42 -> 42,000,000

        usd:
        192 -> 192,000

        """


        if value is None:

            return None



        value = float(value)



        if price_type == "mesghal":


            if value < 1000:

                return value * 1000000



        if price_type == "usd":


            if value < 1000:

                return value * 1000



        return value



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
                "مظنه" in name
                or
                "آبشده" in name

            ):


                price = self.normalize_price(

                    price,

                    "mesghal"

                )


                if price:

                    data[
                        "mesghal_price"
                    ] = price




            # دلار آزاد


            elif (

                "usd" in symbol
                or
                "dollar" in symbol
                or
                "دلار" in name

            ):


                price = self.normalize_price(

                    price,

                    "usd"

                )


                if price:

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


            r'"value"\s*:\s*"?([0-9\.]+)"?'


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
