import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Market Parser v2

    Extracts market rows from Next.js payload
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


            for index, payload in enumerate(payloads):

                if '"rows"' in payload and '"lastPrice"' in payload:

                    print(
                        "MARKET PAYLOAD FOUND:",
                        index
                    )


                    rows = self.extract_rows(payload)


                    print(
                        "ROWS FOUND:",
                        len(rows)
                    )


                    result.update(
                        self.map_rows(rows)
                    )



                if "xau" in payload.lower():

                    xau = self.extract_number(
                        payload,
                        "xau"
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
                "Parser Error:",
                e
            )

            return {}



    def extract_rows(self, text):

        rows = []


        pattern = (
            r'"symbol":"(.*?)".*?'
            r'"persianName":"(.*?)".*?'
            r'"lastPrice":"(.*?)".*?'
            r'"change":"(.*?)".*?'
            r'"changePercent":"(.*?)"'
        )


        matches = re.findall(
            pattern,
            text
        )


        for m in matches:

            rows.append({

                "symbol":m[0],
                "name":m[1],
                "price":m[2],
                "change":m[3],
                "percent":m[4]

            })


        return rows



    def clean(self, value):

        try:

            return float(
                value
                .replace(",","")
                .replace(" ","")
            )

        except:

            return None



    def map_rows(self, rows):

        data={}


        for row in rows:

            symbol=row["symbol"].lower()

            price=self.clean(
                row["price"]
            )


            name=row["name"]



            print(
                "ROW:",
                symbol,
                name,
                price
            )


            if "18" in symbol or "هجده" in name:

                data["gold18_price"]=price



            if (
                "mesghal" in symbol
                or
                "abshode" in symbol
                or
                "مظنه" in name
            ):

                data["mesghal_price"]=price



            if (
                "usd" in symbol
                or
                "dollar" in symbol
                or
                "دلار" in name
            ):

                data["usd_free_rate"]=price



            if "emami" in symbol:

                data["coin_emami"]=price



            if "bahar" in symbol:

                data["coin_bahar"]=price



        return data



    def extract_number(self,text,key):

        match=re.search(
            key+r'.{0,50}?([0-9]{3,6})',
            text,
            re.I
        )


        if match:

            try:
                return float(
                    match.group(1)
                )

            except:
                pass


        return None
