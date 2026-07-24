import re
import json
import html
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Parser V17

    Stable parser for Next.js payloads.
    """

    def parse(
        self,
        raw_html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        result = {}

        try:

            print("######## FARAZ PARSER V17 DEBUG ########")
            print("SOURCE:", source)


            payloads = re.findall(
                r'self\.__next_f\.push\((.*?)\)</script>',
                raw_html,
                re.DOTALL
            )


            print(
                "PAYLOAD COUNT:",
                len(payloads)
            )


            decoded = []


            for p in payloads:

                try:

                    text = (
                        p
                        .encode(
                            "utf-8"
                        )
                        .decode(
                            "unicode_escape"
                        )
                    )

                    decoded.append(text)

                except:

                    decoded.append(p)



            full_text = "\n".join(decoded)



            full_text = html.unescape(
                full_text
            )



            if source == "market":

                rows = self.extract_market_rows(
                    full_text
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
                    full_text
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



    def extract_market_rows(
        self,
        text
    ):

        rows = []


        pattern = re.compile(

            r'"symbol"\s*:\s*"([^"]+)".{0,300}?'
            r'"persianName"\s*:\s*"([^"]+)".{0,300}?'
            r'"lastPrice"\s*:\s*"?([\d\.]+)"?',

            re.DOTALL

        )



        matches = pattern.findall(
            text
        )



        for symbol,name,price in matches:

            rows.append({

                "symbol":symbol,

                "name":name,

                "price":price

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

            price=self.clean(
                row["price"]
            )


            print(
                "ROW:",
                symbol,
                name,
                price
            )


            if price is None:
                continue


            if (

                "abshode" in symbol
                or
                "مظنه" in name
                or
                "آبشده" in name

            ):

                if price > 1000000:

                    data[
                        "mesghal_price"
                    ] = price



            if (

                "usd" in symbol
                or
                "دلار" in name

            ):

                if price > 10000:

                    data[
                        "usd_free_rate"
                    ] = price



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

                value=self.clean(
                    m.group(1)
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
            )

        except:

            return None
