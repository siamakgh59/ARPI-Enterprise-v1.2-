import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Parser V23

    Stable parser based on Next.js payload structures.
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

            print("######## FARAZ PARSER V23 DEBUG ########")
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


            for index, payload in enumerate(payloads):


                if source == "market":

                    if '"rows":[' in payload:

                        print(
                            "MARKET ROW PAYLOAD:",
                            index
                        )


                        rows = self.extract_market_rows(
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
                "################################"
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
        text
    ):

        try:

            if "Ø" in text or "Ù" in text:

                return (
                    text
                    .encode("latin1")
                    .decode("utf-8")
                )

        except:

            pass


        return text



    def extract_market_rows(
        self,
        payload
    ):


        rows = []


        try:

            match = re.search(
                r'"rows":(\[.*?\]),"currentPage"',
                payload,
                re.DOTALL
            )


            if not match:

                return rows



            raw = match.group(1)


            data = json.loads(
                raw
            )


            for item in data:

                rows.append({

                    "symbol":
                    item.get(
                        "symbol",
                        ""
                    ),

                    "name":
                    self.fix_encoding(
                        item.get(
                            "persianName",
                            ""
                        )
                    ),

                    "price":
                    item.get(
                        "lastPrice"
                    ),

                    "change":
                    item.get(
                        "change"
                    )

                })


        except Exception as e:

            print(
                "ROW PARSE ERROR:",
                e
            )


        return rows



    def clean(
        self,
        value
    ):

        try:

            if value is None:
                return None


            return float(
                str(value)
                .replace(
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


            change = self.clean(
                row["change"]
            )



            print(
                "ROW:",
                symbol,
                name,
                price
            )



            if "abshode" in symbol:

                data[
                    "mesghal_price"
                ] = price



            if (
                "haratnaghdi" in symbol
                or
                "usd" in symbol
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



            if change is not None:

                data[
                    "gold_daily_change"
                ] = change



        return data



    def extract_gold18(
        self,
        payload
    ):


        try:


            match = re.search(
                r'"marketItem":\{(.*?)\}',
                payload,
                re.DOTALL
            )


            if not match:

                return None



            block = match.group(1)



            price = re.search(
                r'"price":(\d+)',
                block
            )


            if price:

                return float(
                    price.group(1)
                )



        except Exception as e:


            print(
                "GOLD18 ERROR:",
                e
            )


        return None
