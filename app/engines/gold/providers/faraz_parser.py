import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz Parser V21

    Robust parser for Faraz.io Next.js payloads

    Extracts:
    - mesghal_price
    - usd_free_rate
    - coin_emami
    - coin_bahar
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
                "######## FARAZ PARSER V21 DEBUG ########"
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


                if (
                    "lastPrice" in payload
                    or
                    "price" in payload
                    or
                    "value" in payload
                ):

                    print(
                        "ACTIVE PAYLOAD:",
                        index
                    )


                    if source == "gold18":

                        price = self.extract_price(
                            payload
                        )

                        if price:

                            result[
                                "gold18_price"
                            ] = price


                    else:


                        rows = self.extract_objects(
                            payload
                        )


                        print(
                            "OBJECT COUNT:",
                            len(rows)
                        )


                        mapped = self.map_objects(
                            rows
                        )


                        result.update(
                            mapped
                        )



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




    def extract_objects(
        self,
        text
    ):

        objects = []


        pattern = r'\{(.*?)\}'


        matches = re.findall(
            pattern,
            text,
            re.DOTALL
        )


        for item in matches:


            if (
                "lastPrice" not in item
                and
                "price" not in item
            ):
                continue



            symbol = self.find_value(
                item,
                "symbol"
            )


            name = (
                self.find_value(
                    item,
                    "persianName"
                )
                or
                self.find_value(
                    item,
                    "name"
                )
            )


            price = (
                self.find_value(
                    item,
                    "lastPrice"
                )
                or
                self.find_value(
                    item,
                    "price"
                )
                or
                self.find_value(
                    item,
                    "value"
                )
            )


            if price:


                objects.append({

                    "symbol":
                        symbol or "",

                    "name":
                        self.decode(
                            name or ""
                        ),

                    "price":
                        self.clean(
                            price
                        )

                })


        return objects





    def find_value(
        self,
        text,
        key
    ):

        pattern = (
            r'"'
            + key +
            r'"\s*:\s*"?(.*?)"?[,}]'
        )


        match = re.search(
            pattern,
            text
        )


        if match:

            return match.group(1)


        return None





    def map_objects(
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



            if price is None:
                continue



            # مظنه آبشده

            if (

                "abshode" in symbol
                or
                "harat" in symbol
                or
                "مظنه" in name
                or
                "آبشده" in name

            ):

                if price > 1000000:

                    data[
                        "mesghal_price"
                    ] = price



            # دلار

            if (

                "usd" in symbol
                or
                "dollar" in symbol

            ):

                data[
                    "usd_free_rate"
                ] = price



            # امامی

            if "emami" in symbol:

                data[
                    "coin_emami"
                ] = price



            # بهار

            if "bahar" in symbol:

                data[
                    "coin_bahar"
                ] = price



        return data





    def extract_price(
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


                if value:

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





    def decode(
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
