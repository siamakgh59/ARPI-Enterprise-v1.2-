import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Next.js Market Parser

    Extract:
    - Global gold
    - Iran gold market
    - Coins
    - USD market

    Compatible with GoldNormalizer
    """

    def parse(
        self,
        html: str
    ) -> Dict[str, Any]:

        result = {}

        try:

            payloads = self._extract_next_payloads(html)

            print("######## FARAZ PARSER DEBUG ########")
            print("PAYLOAD COUNT:", len(payloads))


            for index, payload in enumerate(payloads):

                text = payload.lower()


                keys = []

                for key in [
                    "gold",
                    "usd",
                    "price",
                    "last",
                    "rows"
                ]:

                    if key in text:
                        keys.append(key)


                if keys:

                    print(
                        f"PAYLOAD {index} KEYS:",
                        keys
                    )


                #
                # Global gold extraction
                #

                global_gold = self._extract_xau(payload)

                if global_gold:

                    result["xau_usd"] = global_gold



                #
                # Market rows extraction
                #

                rows = self._extract_rows(payload)


                if rows:

                    print(
                        "FOUND MARKET ROWS:",
                        len(rows)
                    )


                    market_data = self._map_rows(rows)

                    result.update(
                        market_data
                    )



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
                str(e)
            )

            return {}



    def _extract_next_payloads(
        self,
        html: str
    ):

        return re.findall(
            r'self\.__next_f\.push\((.*?)\)</script>',
            html,
            re.DOTALL
        )



    def _extract_xau(
        self,
        text: str
    ):

        patterns = [

            r'"xau[^0-9]{0,30}([0-9]{3,6})',

            r'"ounce[^0-9]{0,30}([0-9]{3,6})',

        ]


        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                try:
                    return float(
                        match.group(1)
                    )

                except:
                    pass


        return None



    def _extract_rows(
        self,
        text: str
    ):

        rows = []


        matches = re.findall(

            r'\{"id":\d+,"symbol":"(.*?)".*?"lastPrice":"(.*?)".*?"change":"(.*?)".*?"changePercent":"(.*?)".*?"trend":"(.*?)".*?\}',

            text

        )


        for item in matches:

            symbol, price, change, percent, trend = item


            rows.append({

                "symbol": symbol,

                "lastPrice": price,

                "change": change,

                "changePercent": percent,

                "trend": trend

            })


        return rows



    def _clean_number(
        self,
        value
    ):

        if value is None:

            return None


        try:

            value = (
                str(value)
                .replace(",", "")
                .replace(" ", "")
            )


            return float(value)


        except:

            return None



    def _map_rows(
        self,
        rows
    ) -> Dict:


        result = {}


        for row in rows:


            symbol = row["symbol"].lower()


            price = self._clean_number(
                row["lastPrice"]
            )


            change = self._clean_number(
                row["change"]
            )


            #
            # Gold 18 Iran
            #

            if any(
                x in symbol
                for x in [
                    "geram18",
                    "gold18",
                    "geramtil",
                    "geram"
                ]
            ):

                result["gold18_price"] = price



            #
            # Mesghal
            #

            if any(
                x in symbol
                for x in [
                    "mesghal",
                    "abshode"
                ]
            ):

                result["mesghal_price"] = price



            #
            # USD
            #

            if any(
                x in symbol
                for x in [
                    "usd",
                    "dollar",
                    "harat"
                ]
            ):

                result["usd_free_rate"] = price



                if change is not None:

                    result["usd_change"] = change



            #
            # Coins
            #

            if "emami" in symbol:

                result["coin_emami"] = price



            if "bahar" in symbol:

                result["coin_bahar"] = price



            #
            # Daily change
            #

            if change is not None:

                result["gold_daily_change"] = change



        return result
