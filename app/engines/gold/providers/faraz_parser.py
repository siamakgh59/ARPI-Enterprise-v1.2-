import re
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Market Parser v4

    Extract:
    - gold18_price
    - mesghal_price
    - usd_free_rate
    - coin_emami
    - coin_bahar
    - xau_usd
    """

    def parse(self, html: str) -> Dict[str, Any]:

        result = {}

        try:

            payloads = re.findall(
                r'self\.__next_f\.push\((.*?)\)</script>',
                html,
                re.DOTALL
            )

            print("######## FARAZ PARSER DEBUG ########")
            print("PAYLOAD COUNT:", len(payloads))


            decoded_payloads = []


            for index, payload in enumerate(payloads):

                try:
                    decoded = payload.encode(
                        "utf-8"
                    ).decode(
                        "unicode_escape"
                    )

                except:
                    decoded = payload


                decoded_payloads.append(decoded)


                keys=[]

                for k in [
                    "rows",
                    "lastPrice",
                    "gold",
                    "usd"
                ]:
                    if k.lower() in decoded.lower():
                        keys.append(k)


                if keys:
                    print(
                        f"PAYLOAD {index} KEYS:",
                        keys
                    )



            for payload in decoded_payloads:


                if (
                    "symbol" in payload
                    and
                    "lastPrice" in payload
                ):

                    rows = self.extract_rows(
                        payload
                    )


                    print(
                        "ROWS FOUND:",
                        len(rows)
                    )


                    result.update(
                        self.map_rows(rows)
                    )



                if "xau" in payload.lower():

                    xau = self.extract_xau(
                        payload
                    )

                    if xau:
                        result["xau_usd"] = xau



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
                e
            )

            return {}




    def extract_rows(
        self,
        text
    ):

        rows=[]


        pattern = (
            r'"symbol":"([^"]+)".*?'
            r'"persianName":"([^"]+)".*?'
            r'"lastPrice":"([^"]+)"'
        )


        matches = re.findall(
            pattern,
            text,
            re.DOTALL
        )


        for m in matches:

            rows.append(
                {
                    "symbol":m[0],
                    "name":m[1],
                    "price":m[2]
                }
            )


        return rows




    def clean(
        self,
        value
    ):

        try:

            return float(
                value
                .replace(",","")
                .replace(" ","")
            )

        except:

            return None




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



            #
            # Gold 18
            #

            if any(
                x in symbol
                for x in [
                    "gold18",
                    "geram18",
                    "geramtala18",
                    "tala18"
                ]
            ):

                data["gold18_price"]=price



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

                data["mesghal_price"]=price



            #
            # USD Iran
            #

            if any(
                x in symbol
                for x in [
                    "usdhrt",
                    "usdteh",
                    "dollar",
                    "usd"
                ]
            ):

                if price and price > 100000:

                    data["usd_free_rate"]=price



            #
            # Coins
            #

            if any(
                x in symbol
                for x in [
                    "emami",
                    "coinemami"
                ]
            ):

                data["coin_emami"]=price



            if any(
                x in symbol
                for x in [
                    "bahar",
                    "coinbahar"
                ]
            ):

                data["coin_bahar"]=price



        return data




    def extract_xau(
        self,
        text
    ):

        patterns=[

            r'xau.{0,50}?([0-9]{3,6})',

            r'ounce.{0,50}?([0-9]{3,6})'

        ]


        for p in patterns:

            m=re.search(
                p,
                text,
                re.I
            )

            if m:

                try:
                    return float(
                        m.group(1)
                    )

                except:
                    pass


        return None
