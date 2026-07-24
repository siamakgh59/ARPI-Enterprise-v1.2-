import re
import json
from typing import Dict, Any


class FarazParser:

    """
    Faraz Parser V12

    Stable parser based on:
    - Next.js payload extraction
    - Flexible row detection
    """


    MESGHAL_FACTOR = 4.0715


    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        result = {}

        print("######## FARAZ PARSER V12 DEBUG ########")
        print("SOURCE:", source)


        try:

            payloads = re.findall(
                r'self\.__next_f\.push\((.*?)\)</script>',
                html,
                re.DOTALL
            )


            print(
                "PAYLOAD COUNT:",
                len(payloads)
            )


            for i,payload in enumerate(payloads):


                decoded = (
                    payload
                    .replace('\\"','"')
                )


                if "rows" in decoded:

                    print(
                        "ROWS PAYLOAD:",
                        i
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


                    price = self.extract_price(
                        decoded
                    )


                    if price:

                        result[
                            "gold18_price"
                        ] = price



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
                    self.MESGHAL_FACTOR
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
                "PARSER ERROR:",
                e
            )

            return {}



    def extract_rows(
        self,
        text
    ):

        rows=[]


        # flexible matcher

        pattern = re.compile(

            r'"symbol"\s*:\s*"([^"]+)".{0,500}?'
            r'"(?:persianName|name)"\s*:\s*"([^"]+)".{0,500}?'
            r'"lastPrice"\s*:\s*"?([\d\.]+)"?',

            re.DOTALL

        )


        for m in pattern.findall(text):


            rows.append({

                "symbol":m[0],

                "name":
                    self.fix_encoding(
                        m[1]
                    ),

                "price":
                    self.clean(
                        m[2]
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

            r'"lastPrice"\s*:\s*"?([\d\.]+)"?',

            r'"price"\s*:\s*"?([\d\.]+)"?',

            r'"value"\s*:\s*"?([\d\.]+)"?'

        ]


        for p in patterns:


            m=re.search(
                p,
                text
            )


            if m:

                return self.clean(
                    m.group(1)
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
