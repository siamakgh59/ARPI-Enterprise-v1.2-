import re
import json
from typing import Dict, Any


class CoinParser:
    """
    Faraz Coin Parser V39

    Extract:
    - coin_emami
    - coin_bahar
    - coin_bubble

    Compatible with:
    faraz.io/markets/gold-currency?page=2
    """


    def parse(
        self,
        html: str,
        source: str = "coin"
    ) -> Dict[str, Any]:

        print("######## COIN PARSER V39 DEBUG ########")
        print("SOURCE:", source)

        result = {}

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


            for payload in payloads:

                decoded = (
                    payload
                    .replace('\\"', '"')
                    .replace('\\\\', '\\')
                )


                rows = self.extract_rows_array(
                    decoded
                )


                if rows:

                    print(
                        "COIN ROWS FOUND:",
                        len(rows)
                    )

                    self.parse_rows(
                        rows,
                        result
                    )


            self.calculate_coin_bubble(
                result
            )


            print(
                "FINAL COIN RESULT:",
                result
            )


        except Exception as e:

            print(
                "COIN PARSER ERROR:",
                e
            )


        print(
            "################################"
        )


        return result



    def extract_rows_array(
        self,
        text: str
    ):

        try:

            positions = [
                m.start()
                for m in re.finditer(
                    r'"rows":',
                    text
                )
            ]


            for pos in positions:

                start = text.find(
                    '[',
                    pos
                )


                if start == -1:
                    continue


                depth = 0


                for i in range(
                    start,
                    len(text)
                ):

                    if text[i] == '[':

                        depth += 1


                    elif text[i] == ']':
                        
                        depth -= 1


                        if depth == 0:

                            try:

                                return json.loads(
                                    text[start:i+1]
                                )

                            except:

                                continue


        except Exception as e:

            print(
                "ROWS ERROR:",
                e
            )


        return []



    def parse_rows(
        self,
        rows,
        result: Dict
    ):


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
            ).lower()


            price = self.clean(
                row.get(
                    "lastPrice"
                )
            )


            print(
                "COIN ROW:",
                symbol,
                name,
                price
            )



            # -------------------------
            # Coin Emami
            # -------------------------

            if (

                "sekkefardayi" in symbol

                and

                "hobab" not in symbol

            ):

                result[
                    "coin_emami"
                ] = price


                print(
                    "COIN EMAMI FOUND:",
                    price
                )



            # -------------------------
            # Coin Bahar / نقدی
            # -------------------------

            elif (

                "sekkenaghdi" in symbol

                and

                "hobab" not in symbol

            ):

                result[
                    "coin_bahar"
                ] = price


                print(
                    "COIN BAHAR FOUND:",
                    price
                )



            # fallback Persian

            elif (

                "سکه نقدی" in name

                and

                result.get(
                    "coin_bahar"
                ) is None

            ):

                result[
                    "coin_bahar"
                ] = price



    def calculate_coin_bubble(
        self,
        result: Dict
    ):

        coin = result.get(
            "coin_emami"
        )


        if coin:

            # اگر mesghal بعداً از Provider اضافه شد
            # این قسمت فعال می‌شود

            pass



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
                .replace(
                    "%",
                    ""
                )
            )


        except:

            return None
