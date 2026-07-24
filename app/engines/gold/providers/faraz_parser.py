import re
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Parser V11

    Extract:
    - Mesghal price
    - Gold 18 price
    - USD
    - Coins

    Strategy:
    Persian name priority
    Symbol secondary
    """

    MESGHAL_FACTOR = 4.0715


    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        result = {}

        try:

            print("######## FARAZ PARSER V11 DEBUG ########")
            print("SOURCE:", source)


            payloads = re.findall(
                r'self\.__next_f\.push\((.*?)\)</script>',
                html,
                re.DOTALL
            )


            print(
                "PAYLOAD COUNT:",
                len(payloads)
            )


            for payload in payloads:


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


                    result.update(
                        self.map_rows(rows)
                    )


                if source == "gold18":


                    gold18 = self.extract_price(
                        payload
                    )


                    if gold18:

                        result[
                            "gold18_price"
                        ] = gold18



            # محاسبه fallback
            if (
                "gold18_price" not in result
                and
                "mesghal_price" in result
            ):

                result[
                    "gold18_price"
                ] = round(
                    result["mesghal_price"]
                    /
                    self.MESGHAL_FACTOR,
                    0
                )


            print(
                "FINAL RESULT:",
                result
            )

            print(
                "################################"
            )


            return result


        except Exception as e:

            print(
                "Parser Error:",
                e
            )

            return {}



    def extract_rows(
        self,
        text
    ):

        rows=[]


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

                "symbol":m[0],

                "name":
                    self.fix_encoding(
                        m[1]
                    ),

                "price":
                    self.clean(
                        m[3]
                    )

            })


        return rows



    def map_rows(
        self,
        rows
    ):

        data={}


        for row in rows:


            symbol=row["symbol"].lower()

            name=row["name"]

            price=row["price"]


            print(
                "ROW:",
                symbol,
                name,
                price
            )


            # مظنه آبشده
            if (
                "مظنه" in name
                or
                "آبشده" in name
                or
                "abshode" in symbol
            ):

                data[
                    "mesghal_price"
                ] = price



            # دلار
            elif (
                "دلار" in name
                or
                "usd" in symbol
            ):

                data[
                    "usd_free_rate"
                ] = price



            elif "emami" in symbol:

                data[
                    "coin_emami"
                ] = price



            elif "bahar" in symbol:

                data[
                    "coin_bahar"
                ] = price



        return data



    def extract_price(
        self,
        text
    ):

        patterns=[

            r'"lastPrice":("?)([\d\.]+)\1',

            r'"price":("?)([\d\.]+)\1',

            r'"value":("?)([\d\.]+)\1'

        ]


        for p in patterns:


            m=re.search(
                p,
                text
            )


            if m:

                return self.clean(
                    m.group(2)
                )


        return None



    def clean(
        self,
        value
    ):

        try:

            return float(
                str(value)
                .replace(",","")
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
                    .encode("latin1")
                    .decode("utf-8")
                )

        except:

            pass


        return text
