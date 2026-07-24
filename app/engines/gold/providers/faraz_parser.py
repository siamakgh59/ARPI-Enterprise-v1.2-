import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz Gold Parser V6

    Extract:
    - XAU/USD
    - Gold 18
    - Mesghal
    - USD
    - Coins

    Compatible with Next.js escaped payload
    """

    def parse(self, html: str) -> Dict[str, Any]:

        result = {}

        print("######## FARAZ PARSER V6 DEBUG ########")


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


                if "rows" not in payload:
                    continue


                print(
                    "MARKET PAYLOAD FOUND:",
                    i
                )


                rows = self.extract_rows(
                    payload
                )


                print(
                    "ROWS FOUND:",
                    len(rows)
                )


                mapped = self.map_rows(
                    rows
                )


                result.update(
                    mapped
                )



                # XAU
                xau = self.extract_xau(
                    payload
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
                "PARSER ERROR:",
                e
            )


            return {}





    def extract_rows(
        self,
        text
    ):


        rows=[]


        pattern = re.compile(

            r'\\"symbol\\":\\"(.*?)\\".*?'
            r'\\"persianName\\":\\"(.*?)\\".*?'
            r'\\"lastPrice\\":\\"(.*?)\\"',

            re.DOTALL

        )


        matches = pattern.findall(
            text
        )



        for m in matches:


            rows.append({

                "symbol":m[0],
                "name":m[1],
                "price":m[2]

            })


        return rows





    def clean(
        self,
        value
    ):


        try:

            return float(

                value
                .replace(",","")
                .strip()

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
                price
            )



            # طلای 18 عیار

            if (

                "geramTalaHejdah".lower()
                in symbol

                or

                "18" in symbol

                or

                "هجده" in name

            ):

                data["gold18_price"]=price



            # مظنه

            if (

                "mesghal" in symbol

                or

                "abshode" in symbol

                or

                "مظنه" in name

            ):

                data["mesghal_price"]=price



            # دلار

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





    def extract_xau(
        self,
        text
    ):


        match=re.search(

            r'xau.{0,100}?([0-9]{3,6})',

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
