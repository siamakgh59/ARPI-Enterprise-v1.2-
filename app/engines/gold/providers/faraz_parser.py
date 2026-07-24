import re
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Market Parser v3

    Responsibilities:
    - Parse Next.js payload
    - Extract market rows
    - Map symbols into ARPI Gold schema
    - Avoid dependency on Persian text encoding
    """


    def parse(self, html: str) -> Dict[str, Any]:

        result = {}

        try:

            payloads = re.findall(
                r'self\.__next_f\.push\((.*?)\)</script>',
                html,
                re.DOTALL
            )


            print("######## FARAZ PARSER DEBUG ########")
            print("PAYLOAD COUNT:", len(payloads))


            for index, payload in enumerate(payloads):


                # Detect market rows

                if (
                    '"rows"' in payload
                    and '"lastPrice"' in payload
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


                    for row in rows:

                        print(
                            "ROW:",
                            row["symbol"],
                            row["price"]
                        )


                    mapped = self.map_rows(
                        rows
                    )


                    result.update(
                        mapped
                    )



                # Global gold price

                if (
                    "xau" in payload.lower()
                    or
                    "goldprice" in payload.lower()
                ):

                    xau = self.extract_xau(
                        payload
                    )

                    if xau:

                        result["xau_usd"] = xau



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
                e
            )

            return {}



    def extract_rows(
        self,
        text: str
    ):

        rows = []


        pattern = (
            r'"symbol":"(.*?)".*?'
            r'"persianName":"(.*?)".*?'
            r'"lastPrice":"(.*?)".*?'
            r'"change":"(.*?)".*?'
            r'"changePercent":"(.*?)"'
        )


        matches = re.findall(
            pattern,
            text,
            re.DOTALL
        )


        for item in matches:

            rows.append({

                "symbol": item[0],
                "name": item[1],
                "price": item[2],
                "change": item[3],
                "percent": item[4]

            })


        return rows



    def clean_number(
        self,
        value
    ):

        try:

            value = (
                value
                .replace(",", "")
                .replace(" ", "")
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


            price = self.clean_number(
                row["price"]
            )


            if price is None:

                continue



            #
            # مظنه آبشده
            #

            if (
                "abshode" in symbol
                or
                "mesghal" in symbol
            ):

                data[
                    "mesghal_price"
                ] = price



            #
            # دلار آزاد
            #

            if (
                "usdhrt" in symbol
                or
                "usdteh" in symbol
                or
                "dollar" in symbol
            ):

                if (
                    "f" not in symbol
                    or
                    "naghdi" in symbol
                ):

                    data[
                        "usd_free_rate"
                    ] = price



            #
            # گرم نقره حذف شود
            #

            if (
                "noghre" in symbol
            ):

                continue



            #
            # سکه امامی
            #

            if (
                "emami" in symbol
            ):

                data[
                    "coin_emami"
                ] = price



            #
            # سکه بهار
            #

            if (
                "bahar" in symbol
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

            r'xau.{0,100}?([0-9]{3,6}\.?[0-9]*)',

            r'gold.{0,100}?([0-9]{3,6}\.?[0-9]*)'

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
