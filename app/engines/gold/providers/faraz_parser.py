import re
import json
from typing import Dict, Any


class FarazParser:

    """
    Faraz Gold Parser V24

    Supports:
    - market gold-currency page
    - gold18 detail page

    Extract:
    - mesghal_price
    - usd_free_rate
    - gold18_price
    - volume
    - daily change
    """


    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:


        result = {}

        print("######## FARAZ PARSER V24 DEBUG ########")
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


                if (
                    "rows" in payload
                    or
                    "marketItem" in payload
                    or
                    "lastPrice" in payload
                ):


                    print(
                        "ACTIVE PAYLOAD:",
                        i
                    )


                    decoded = self.decode_payload(
                        payload
                    )


                    if decoded:


                        if source=="market":

                            data = self.extract_market(
                                decoded
                            )

                            result.update(data)


                        if source=="gold18":

                            data = self.extract_gold18(
                                decoded
                            )

                            result.update(data)



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



    def decode_payload(
        self,
        payload
    ):


        try:

            start = payload.find(
                "{"
            )


            end = payload.rfind(
                "}"
            )


            if start==-1 or end==-1:

                return None


            raw = payload[start:end+1]


            raw = (
                raw
                .replace('\\"','"')
            )


            return raw


        except Exception as e:

            print(
                "DECODE ERROR",
                e
            )

            return None




    def extract_market(
        self,
        text
    ):


        result={}


        try:


            rows_match = re.search(
                r'"rows":(\[.*?\]),"currentPage"',
                text,
                re.DOTALL
            )


            if not rows_match:

                return {}


            rows_json = rows_match.group(1)


            rows_json = (
                rows_json
                .replace('\\"','"')
            )


            rows = json.loads(
                rows_json
            )


            print(
                "ROWS:",
                len(rows)
            )



            for row in rows:


                symbol = (
                    row.get(
                        "symbol",
                        ""
                    )
                    .lower()
                )


                name = row.get(
                    "persianName",
                    ""
                )


                price = self.clean(
                    row.get(
                        "lastPrice"
                    )
                )


                print(
                    "ROW:",
                    symbol,
                    name,
                    price
                )


                if (
                    "abshode" in symbol
                    or
                    "آبشده" in name
                    or
                    "مظنه" in name
                ):

                    result[
                        "mesghal_price"
                    ] = price



                if (
                    "harat" in symbol
                    or
                    "usd" in symbol
                ):

                    result[
                        "usd_free_rate"
                    ] = price



                if (
                    "emami" in symbol
                ):

                    result[
                        "coin_emami"
                    ] = price



                if (
                    "bahar" in symbol
                ):

                    result[
                        "coin_bahar"
                    ] = price



                if (
                    "changePercent" in row
                ):

                    result[
                        "gold_daily_change"
                    ] = row.get(
                        "changePercent"
                    )


            return result



        except Exception as e:

            print(
                "MARKET ERROR:",
                e
            )

            return {}




    def extract_gold18(
        self,
        text
    ):


        result={}


        try:


            price = re.search(
                r'"lastPrice\\?":?\\?"?([0-9]+)',
                text
            )


            if price:

                result[
                    "gold18_price"
                ] = float(
                    price.group(1)
                )


            volume = re.search(
                r'"volume\\?":?\\?"?([0-9]+)',
                text
            )


            if volume:

                result[
                    "volume"
                ] = float(
                    volume.group(1)
                )


            change = re.search(
                r'"changePercent\\?":?\\?"?([-0-9\.]+)',
                text
            )


            if change:

                result[
                    "gold_daily_change"
                ] = float(
                    change.group(1)
                )


            return result



        except Exception as e:

            print(
                "GOLD18 ERROR:",
                e
            )

            return {}




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
