# app/engines/gold/providers/faraz_parser.py

import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Gold Market Parser V5

    Extracts market data from Next.js stream payload.
    """

    def parse(self, html: str) -> Dict[str, Any]:

        result = {}

        try:

            print("######## FARAZ PARSER V5 DEBUG ########")


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


                decoded = self.decode_text(payload)



                if "rows" in decoded:

                    print(
                        "MARKET PAYLOAD FOUND:",
                        index
                    )


                    rows = self.extract_rows(
                        decoded
                    )


                    print(
                        "ROWS FOUND:",
                        len(rows)
                    )


                    for row in rows:

                        self.debug_row(row)


                    result.update(
                        self.map_rows(rows)
                    )



                # XAU extraction

                if "xau" in decoded.lower():

                    xau = self.extract_xau(
                        decoded
                    )


                    if xau:

                        result["xau_usd"] = xau



            print(
                "FINAL PARSER RESULT:",
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



    def decode_text(self, text):

        """
        Fix broken UTF8 strings
        """

        try:

            return (
                text
                .encode(
                    "latin1",
                    errors="ignore"
                )
                .decode(
                    "utf-8",
                    errors="ignore"
                )
            )


        except:

            return text



    def extract_rows(self, text):

        rows = []


        pattern = r'\{[^{}]*?"symbol".*?"lastPrice".*?\}'


        matches = re.findall(
            pattern,
            text,
            re.DOTALL
        )


        for item in matches:


            try:

                symbol = self.extract_field(
                    item,
                    "symbol"
                )

                name = self.extract_field(
                    item,
                    "persianName"
                )

                price = self.extract_field(
                    item,
                    "lastPrice"
                )

                change = self.extract_field(
                    item,
                    "change"
                )


                if symbol:

                    rows.append({

                        "symbol": symbol,

                        "name": name,

                        "price": price,

                        "change": change

                    })


            except:

                continue



        return rows



    def extract_field(
        self,
        text,
        key
    ):


        pattern = (
            r'"'
            +
            key
            +
            r'"\s*:\s*"([^"]*)"'
        )


        match = re.search(
            pattern,
            text
        )


        if match:

            return match.group(1)


        return None



    def clean_number(self,value):

        if value is None:

            return None


        try:

            value = (
                value
                .replace(",","")
                .replace(" ","")
                .replace("+","")
            )


            return float(value)


        except:


            return None



    def map_rows(self, rows):

        data = {}



        for row in rows:


            symbol = (
                row["symbol"]
                .lower()
                .strip()
            )


            name = (
                row["name"]
                or ""
            )


            price = self.clean_number(
                row["price"]
            )



            if price is None:

                continue



            # طلای 18 عیار

            if (

                "hejdah" in symbol

                or

                "18" in symbol

                or

                "geramtala" in symbol

                or

                "گرم طلا" in name

            ):

                data["gold18_price"] = price



            # مظنه آب شده

            if (

                "mesghal" in symbol

                or

                "abshode" in symbol

                or

                "مظنه" in name

            ):

                data["mesghal_price"] = price



            # دلار آزاد

            if (

                "usd" in symbol

                or

                "dollar" in symbol

                or

                "دلار" in name

            ):

                data["usd_free_rate"] = price



            # سکه امامی

            if "emami" in symbol:

                data["coin_emami"] = price



            # سکه بهار

            if "bahar" in symbol:

                data["coin_bahar"] = price



        return data



    def extract_xau(self,text):

        patterns = [

            r'"xau_usd".{0,50}?([0-9]+)',

            r'"xau".{0,50}?([0-9]+)'

        ]


        for p in patterns:


            m = re.search(
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



    def debug_row(self,row):

        print(
            "ROW:",
            row
        )
