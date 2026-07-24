import re
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Parser V8

    Robust parser for Next.js payload

    Sources:
    - market
    - gold18

    Extracts:
    - mesghal_price
    - usd_free_rate
    - coin prices
    - gold18_price
    """

    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        result = {}

        try:

            print(
                "######## FARAZ PARSER V8 DEBUG ########"
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


                        print(
                            "MARKET PAYLOAD FOUND:",
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



                elif source == "gold18":


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
                    .encode("latin1")
                    .decode("utf-8")
                )


        except:

            pass


        return text



    def extract_rows(
        self,
        text: str
    ):


        rows = []


        # مستقل از ترتیب فیلدها

        blocks = re.findall(
            r'\{(.*?)\}',
            text,
            re.DOTALL
        )


        for block in blocks:


            if (
                "symbol" not in block
                or
                "lastPrice" not in block
            ):

                continue



            symbol = self.extract_field(
                block,
                "symbol"
            )


            name = (
                self.extract_field(
                    block,
                    "persianName"
                )
                or
                self.extract_field(
                    block,
                    "name"
                )
            )


            price = self.extract_field(
                block,
                "lastPrice"
            )


            if symbol and price:


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



    def extract_field(
        self,
        text,
        key
    ):


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



    def extract_gold18(
        self,
        text
    ):


        # اول دنبال عنوان طلای 18 عیار می‌گردیم

        patterns = [

            r'"lastPrice"\s*:\s*"([0-9\.]+)"',

            r'"price"\s*:\s*"([0-9\.]+)"',

            r'"value"\s*:\s*"([0-9\.]+)"'

        ]


        for pattern in patterns:


            matches = re.findall(
                pattern,
                text
            )


            for value in matches:


                number = self.clean(
                    value
                )


                # حذف اعداد کوچک غیرقیمت

                if number and number > 100000:

                    return number



        return None
