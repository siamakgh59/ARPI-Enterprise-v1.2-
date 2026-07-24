import re
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Parser V16

    Stable Parser for ARPI Gold Intelligence Engine

    Supports:

    - Faraz Next.js self.__next_f payloads
    - Market rows extraction
    - Gold18 detail extraction
    - Unit normalization
    - Iranian gold market symbols

    Output:

    gold18_price
    mesghal_price
    usd_free_rate
    coin_emami
    coin_bahar
    """

    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        result = {}

        try:

            print(
                "######## FARAZ PARSER V16 DEBUG ########"
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
                e
            )


            return {}



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
                    name,

                "price":
                    price

            })


        return rows



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
        kind
    ):


        if value is None:

            return None


        value = float(value)



        #
        # Faraz compressed units
        #

        # مظنه
        if kind == "mesghal":


            if value < 1000000:

                value *= 1000000



        # دلار
        elif kind == "usd":


            if value < 1000:

                value *= 1000



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



            #
            # مظنه آبشده جهانی
            #

            if (

                "abshode" in symbol
                or
                "مظنه" in name
                or
                "آبشده" in name

            ):


                normalized = self.normalize_price(

                    price,

                    "mesghal"

                )


                if normalized:


                    data[
                        "mesghal_price"
                    ] = normalized



            #
            # دلار آزاد
            #

            elif (

                "usd" in symbol
                or
                "hrt" in symbol
                or
                "dollar" in symbol
                or
                "دلار" in name

            ):


                normalized = self.normalize_price(

                    price,

                    "usd"

                )


                print(
                    "USD NORMALIZED:",
                    normalized
                )


                if normalized:


                    data[
                        "usd_free_rate"
                    ] = normalized




            #
            # سکه امامی
            #

            elif "emami" in symbol:


                data[
                    "coin_emami"
                ] = price



            #
            # سکه بهار
            #

            elif "bahar" in symbol:


                data[
                    "coin_bahar"
                ] = price



        print(
            "MAP RESULT:",
            data
        )


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
