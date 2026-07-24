import re
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Parser V13

    Responsibilities:
    - Parse Faraz Next.js payloads
    - Extract:
        * Mesghal (Muzaneh Abshode)
        * USD Free Rate
        * Gold 18K price

    Designed for ARPI Gold Engine.
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
                "######## FARAZ PARSER V13 DEBUG ########"
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
                            "ROWS FOUND:",
                            len(rows)
                        )


                        mapped = self.map_rows(
                            rows
                        )


                        result.update(
                            mapped
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
    ) -> str:


        try:

            if "Ù" in text:

                return (
                    text
                    .encode("latin1")
                    .decode("utf-8")
                )

        except:

            pass


        return text



    def extract_rows(
        self,
        payload: str
    ):


        rows = []


        pattern = (

            r'"symbol":"(.*?)".*?'
            r'"persianName":"(.*?)".*?'
            r'"lastPrice":("?)([\d\.]+)\3'

        )


        matches = re.findall(
            pattern,
            payload,
            re.DOTALL
        )


        for item in matches:


            price = self.clean(
                item[3]
            )


            if price is None:
                continue


            rows.append({

                "symbol":
                    item[0],

                "name":
                    self.fix_encoding(
                        item[1]
                    ),

                "price":
                    price

            })


        return rows



    def clean(
        self,
        value
    ):


        try:

            value = float(
                str(value)
                .replace(",","")
            )


            return value


        except:

            return None



    def validate_price(
        self,
        key,
        value
    ):


        if value is None:

            return False



        # جلوگیری از Fragment اشتباه
        if key == "mesghal_price":


            if value < 1_000_000:

                return False



        if key == "usd_free_rate":


            if value < 10_000:

                return False



        if key == "gold18_price":


            if value < 1_000_000:

                return False



        return True



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


            price = row["price"]



            print(
                "ROW:",
                symbol,
                name,
                price
            )



            # --------------------------
            # مظنه آبشده جهانی
            # --------------------------

            if (

                "abshode" in symbol
                or
                "mesghal" in symbol
                or
                "مظنه" in name
                or
                "آبشده" in name

            ):


                if self.validate_price(
                    "mesghal_price",
                    price
                ):

                    data[
                        "mesghal_price"
                    ] = price



            # --------------------------
            # دلار آزاد
            # --------------------------

            if (

                "usd" in symbol
                or
                "dollar" in symbol
                or
                "دلار" in name

            ):


                if self.validate_price(
                    "usd_free_rate",
                    price
                ):


                    data[
                        "usd_free_rate"
                    ] = price



        return data



    def extract_gold18(
        self,
        payload
    ):


        patterns = [


            r'"lastPrice":("?)([\d\.]+)\1',


            r'"price":("?)([\d\.]+)\1',


            r'"value":("?)([\d\.]+)\1'


        ]



        for pattern in patterns:


            matches = re.findall(
                pattern,
                payload
            )


            for match in matches:


                if isinstance(match, tuple):

                    value = match[-1]

                else:

                    value = match



                value = self.clean(
                    value
                )


                if self.validate_price(
                    "gold18_price",
                    value
                ):

                    return value



        return None
