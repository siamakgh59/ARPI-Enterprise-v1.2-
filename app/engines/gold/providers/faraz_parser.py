import re
import html
from typing import Dict, Any



class FarazParser:
    """
    Faraz.io Gold Parser v4

    Supports:

    - gold-currency page
    - geramTalaHejdah page

    Extracts:

    xau_usd
    gold18_price
    mesghal_price
    usd_free_rate
    coin_emami
    coin_bahar
    """



    def parse(
        self,
        sources
    ) -> Dict[str, Any]:


        result = {}


        try:


            print(
                "######## FARAZ PARSER V4 DEBUG ########"
            )


            #
            # Support old single html
            #

            if isinstance(
                sources,
                str
            ):

                sources = {

                    "market":
                    sources

                }



            for name, content in sources.items():


                if isinstance(content, dict):

                    continue



                print(
                    "SOURCE:",
                    name
                )



                payloads = self.extract_payloads(
                    content
                )



                print(
                    "PAYLOAD COUNT:",
                    len(payloads)
                )



                for payload in payloads:


                    rows = self.extract_rows(
                        payload
                    )


                    if rows:


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



                    xau = self.extract_xau(
                        payload
                    )


                    if xau:

                        result[
                            "xau_usd"
                        ] = xau




                #
                # Gold18 direct page
                #

                if name == "gold18":


                    price = self.extract_price(
                        content
                    )


                    if price:


                        result[
                            "gold18_price"
                        ] = price



            print(
                "PARSER RESULT:",
                result
            )


            print(
                "######################################"
            )


            return result



        except Exception as e:


            print(
                "Parser Error:",
                e
            )


            return {}






    def extract_payloads(
        self,
        text
    ):


        payloads = re.findall(

            r'self\.__next_f\.push\((.*?)\)',

            text,

            re.DOTALL

        )


        return payloads






    def extract_rows(
        self,
        text
    ):


        rows = []


        pattern = (

            r'"symbol":"(.*?)".*?'
            r'"persianName":"(.*?)".*?'
            r'"lastPrice":"(.*?)"'

        )


        matches = re.findall(

            pattern,

            text,

            re.DOTALL

        )



        for m in matches:


            rows.append({

                "symbol":
                    m[0],


                "name":
                    self.fix_encoding(m[1]),


                "price":
                    m[2]


            })


        return rows








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


            price = self.clean(
                row["price"]
            )



            if price is None:

                continue



            print(

                "ROW:",

                symbol,

                price

            )




            #
            # Mesghal
            #

            if (

                "abshode" in symbol

                or

                "mesghal" in symbol

            ):


                data[
                    "mesghal_price"
                ] = price




            #
            # USD
            #

            if (

                "usd" in symbol

                or

                "dollar" in symbol

            ):


                data[
                    "usd_free_rate"
                ] = price




            #
            # Coins
            #

            if "emami" in symbol:


                data[
                    "coin_emami"
                ] = price




            if "bahar" in symbol:


                data[
                    "coin_bahar"
                ] = price




        return data








    def extract_price(
        self,
        text
    ):


        patterns = [


            r'"lastPrice":"([0-9,]+)"',


            r'"price":"([0-9,]+)"'


        ]



        for pattern in patterns:


            match = re.search(

                pattern,

                text

            )


            if match:


                return self.clean(

                    match.group(1)

                )



        return None








    def extract_xau(
        self,
        text
    ):


        patterns = [


            r'xau.{0,80}?([0-9]{3,6}\.?[0-9]*)',


            r'"gold".{0,80}?([0-9]{3,6}\.?[0-9]*)'


        ]



        for pattern in patterns:


            match = re.search(

                pattern,

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







    def clean(
        self,
        value
    ):


        try:

            return float(

                value
                .replace(
                    ",",
                    ""
                )

            )


        except:

            return None








    def fix_encoding(
        self,
        text
    ):


        try:


            return (

                html.unescape(text)

            )


        except:


            return text
