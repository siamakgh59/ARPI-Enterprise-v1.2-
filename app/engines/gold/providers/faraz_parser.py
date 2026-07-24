import re
from typing import Dict, Any


class FarazParser:

    """
    Faraz Parser Stable V20

    Supports:
    - Faraz market page
    - Gold18 detail page

    Output:
    ARPI Gold normalized fields
    """

    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        result = {}

        try:

            print("######## FARAZ PARSER V20 DEBUG ########")
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


                if source == "gold18":

                    price = self.extract_price(
                        payload
                    )

                    if price:

                        result[
                            "gold18_price"
                        ] = price


                else:


                    rows = self.extract_rows(
                        payload
                    )


                    if rows:

                        print(
                            "ROWS FOUND:",
                            len(rows)
                        )


                        mapped = self.map_rows(
                            rows
                        )

                        result.update(mapped)



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



    def extract_rows(
        self,
        text
    ):

        rows=[]


        pattern = (

        r'"symbol":"(.*?)".*?'
        r'"persianName":"(.*?)".*?'
        r'"lastPrice":("?)([\d,\.]+)\3'

        )


        matches = re.findall(
            pattern,
            text,
            re.DOTALL
        )


        for m in matches:


            rows.append({

                "symbol":m[0],

                "name":self.decode(
                    m[1]
                ),

                "price":self.clean(
                    m[3]
                )

            })


        return rows



    def decode(
        self,
        text
    ):

        try:

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

            return text



    def clean(
        self,
        value
    ):

        try:

            return float(
                value.replace(
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

        data={}


        for row in rows:


            symbol=row["symbol"].lower()

            name=row["name"]

            price=row["price"]


            print(
                "MAP:",
                symbol,
                name,
                price
            )


            # مظنه آبشده

            if (
                "abshode" in symbol
                or
                "مظنه" in name
                or
                "آبشده" in name
            ):

                if price and price > 1000000:

                    data[
                        "mesghal_price"
                    ]=price



            # دلار

            if (
                "usd" in symbol
                or
                "dollar" in symbol
            ):

                data[
                    "usd_free_rate"
                ]=price



            # سکه

            if "emami" in symbol:

                data[
                    "coin_emami"
                ]=price



            if "bahar" in symbol:

                data[
                    "coin_bahar"
                ]=price



        return data



    def extract_price(
        self,
        text
    ):


        patterns=[

            r'"lastPrice":("?)([\d,\.]+)\1',

            r'"price":("?)([\d,\.]+)\1',

            r'"value":("?)([\d,\.]+)\1'

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
