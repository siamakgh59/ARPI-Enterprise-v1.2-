import re
import json
from typing import Dict, Any, List


class FarazParser:
    """
    Faraz Parser V26 Stable

    هدف:
    استخراج پایدار اطلاعات طلا از Payload های Next.js Faraz

    استخراج:
    - gold18_price
    - mesghal_price
    - usd_free_rate
    - coin_emami
    - coin_bahar
    - gold_daily_change
    - volume
    """

    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        print("######## FARAZ PARSER V26 DEBUG ########")
        print("SOURCE:", source)

        result = {}

        try:

            payloads = self.extract_payloads(
                html
            )

            print(
                "PAYLOAD COUNT:",
                len(payloads)
            )


            for index, payload in enumerate(payloads):

                decoded = self.decode_payload(
                    payload
                )

                if not decoded:
                    continue


                print(
                    "ACTIVE PAYLOAD:",
                    index,
                    "LENGTH:",
                    len(decoded)
                )


                objects = self.extract_objects(
                    decoded
                )


                print(
                    "OBJECT COUNT:",
                    len(objects)
                )


                for obj in objects:


                    if source == "market":

                        self.scan_market_object(
                            obj,
                            result
                        )


                    elif source == "gold18":

                        self.scan_gold18_object(
                            obj,
                            result
                        )



            print(
                "FINAL RESULT:",
                result
            )


        except Exception as e:

            print(
                "PARSER ERROR:",
                e
            )


        print(
            "################################"
        )


        return result



    # -------------------------------
    # Extract Next.js streams
    # -------------------------------

    def extract_payloads(
        self,
        html: str
    ) -> List[str]:

        return re.findall(
            r'self\.__next_f\.push\((.*?)\)</script>',
            html,
            re.DOTALL
        )



    # -------------------------------
    # Decode escaped payload
    # -------------------------------

    def decode_payload(
        self,
        payload: str
    ):

        try:

            text = payload


            text = text.replace(
                '\\"',
                '"'
            )


            text = text.replace(
                '\\\\',
                '\\'
            )


            return text


        except:

            return None



    # -------------------------------
    # Find JSON objects recursively
    # -------------------------------

    def extract_objects(
        self,
        text: str
    ) -> List[dict]:

        objects = []


        matches = re.findall(
            r'\{.*?\}',
            text,
            re.DOTALL
        )


        for item in matches:

            try:

                obj = json.loads(
                    item
                )

                if isinstance(
                    obj,
                    dict
                ):

                    objects.append(
                        obj
                    )


            except:

                continue


        return objects



    # -------------------------------
    # Market scanner
    # -------------------------------

    def scan_market_object(
        self,
        obj: dict,
        result: Dict
    ):


        if "rows" not in obj:

            return


        rows = obj.get(
            "rows"
        )


        if not isinstance(
            rows,
            list
        ):

            return



        print(
            "ROWS FOUND:",
            len(rows)
        )


        for row in rows:


            symbol = str(
                row.get(
                    "symbol",
                    ""
                )
            ).lower()


            name = str(
                row.get(
                    "persianName",
                    ""
                )
            )


            price = self.clean(
                row.get(
                    "lastPrice"
                )
            )


            change = row.get(
                "changePercent"
            )


            print(
                "ROW:",
                symbol,
                price
            )



            # مظنه

            if (
                "abshode" in symbol
                or
                "مظنه" in name
                or
                "آبشده" in name
            ):

                result[
                    "mesghal_price"
                ] = price



            # دلار آزاد

            if (
                "harat" in symbol
                or
                "usd" in symbol
            ):

                result[
                    "usd_free_rate"
                ] = price



            # سکه امامی

            if (
                "emami" in symbol
            ):

                result[
                    "coin_emami"
                ] = price



            # سکه بهار

            if (
                "bahar" in symbol
            ):

                result[
                    "coin_bahar"
                ] = price



            if change:

                try:

                    result[
                        "gold_daily_change"
                    ] = float(
                        str(change)
                        .replace(
                            "%",
                            ""
                        )
                        .replace(
                            "+",
                            ""
                        )
                    )

                except:

                    pass



    # -------------------------------
    # Gold18 scanner
    # -------------------------------

    def scan_gold18_object(
        self,
        obj: dict,
        result: Dict
    ):


        if "price" in obj:


            price = self.clean(
                obj.get(
                    "price"
                )
            )


            if price:

                result[
                    "gold18_price"
                ] = price



        if "volume" in obj:


            volume = self.clean(
                obj.get(
                    "volume"
                )
            )


            if volume:

                result[
                    "volume"
                ] = volume



        if "changePercent" in obj:


            try:

                result[
                    "gold_daily_change"
                ] = float(
                    obj[
                        "changePercent"
                    ]
                )

            except:

                pass



    # -------------------------------
    # Cleaner
    # -------------------------------

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
