import re
import json
from typing import Dict, Any


class FarazParser:

    """
    Faraz Gold Parser V25

    Supports:
    - Faraz gold-currency market
    - Gold 18 detail page

    Extract:
    - mesghal_price
    - usd_free_rate
    - coin_emami
    - coin_bahar
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

        print("######## FARAZ PARSER V25 DEBUG ########")
        print("SOURCE:", source)


        try:

            payloads = re.findall(
                r'self\.__next_f\.push$begin:math:text$\(\.\*\?\)$end:math:text$</script>',
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
                    ):


                        print(
                            "MARKET PAYLOAD:",
                            index
                        )


                        decoded = self.decode(
                            payload
                        )


                        if decoded:


                            data = self.extract_rows(
                                decoded
                            )


                            result.update(
                                data
                            )



                elif source == "gold18":


                    decoded = self.decode(
                        payload
                    )


                    if decoded:


                        data = self.extract_gold18(
                            decoded
                        )


                        result.update(
                            data
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




    def decode(
        self,
        payload
    ):

        try:

            text = (
                payload
                .replace(
                    '\\"',
                    '"'
                )
            )

            return text


        except:

            return payload




    def extract_rows(
        self,
        text
    ):

        result = {}

        try:


            blocks = re.findall(
                r'"rows":($begin:math:display$\.\*\?$end:math:display$)',
                text,
                re.DOTALL
            )


            print(
                "ROWS BLOCKS:",
                len(blocks)
            )


            all_rows = []


            for block in blocks:

                try:

                    rows = json.loads(
                        block
                    )

                    all_rows.extend(
                        rows
                    )


                except:

                    continue



            print(
                "TOTAL ROWS:",
                len(all_rows)
            )



            for row in all_rows:


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


                change = row.get(
                    "changePercent"
                )


                print(
                    "ROW:",
                    symbol,
                    name,
                    price
                )



                # مظنه

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



                # دلار

                if (
                    "usd" in symbol
                    or
                    "harat" in symbol
                ):

                    result[
                        "usd_free_rate"
                    ] = price



                # سکه امامی

                if (
                    "emami" in symbol
                    or
                    "emami" in name.lower()
                ):

                    result[
                        "coin_emami"
                    ] = price



                # سکه بهار آزادی

                if (
                    "bahar" in symbol
                    or
                    "bahar" in name.lower()
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



            return result



        except Exception as e:


            print(
                "ROWS ERROR:",
                e
            )

            return {}




    def extract_gold18(
        self,
        text
    ):

        result = {}


        try:


            price = re.search(
                r'"price":(\d+)',
                text
            )


            if price:

                result[
                    "gold18_price"
                ] = float(
                    price.group(1)
                )



            volume = re.search(
                r'"volume":(\d+)',
                text
            )


            if volume:

                result[
                    "volume"
                ] = float(
                    volume.group(1)
                )



            change = re.search(
                r'"changePercent":(-?\d+\.?\d*)',
                text
            )


            if change:

                result[
                    "gold_daily_change"
                ] = float(
                    change.group(1)
                )



        except Exception as e:

            print(
                "GOLD18 ERROR:",
                e
            )


        return result




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
