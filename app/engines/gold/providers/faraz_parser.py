import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Next.js Payload Parser

    Safe Discovery Version

    Purpose:
    - Extract Next.js payload
    - Discover market data
    - No heavy processing
    """

    SEARCH_KEYS = [
        "xau",
        "gold",
        "ounce",
        "usd",
        "dollar",
        "coin",
        "emami",
        "bahar",
        "mesghal",
        "price"
    ]


    def parse(
        self,
        html: str
    ) -> Dict[str, Any]:

        result = {}

        try:

            print(
                "######## FARAZ PARSER DEBUG ########"
            )


            payloads = self._extract_payloads(
                html
            )


            print(
                "PAYLOAD COUNT:",
                len(payloads)
            )


            for i, payload in enumerate(payloads):


                text = payload


                lower = text.lower()


                found = []


                for key in self.SEARCH_KEYS:

                    if key in lower:

                        found.append(key)



                if found:


                    print(

                        "PAYLOAD",

                        i,

                        "KEYS:",

                        found[:5]

                    )



                extracted = self._extract_values(
                    text
                )


                result.update(
                    extracted
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



    def _extract_payloads(
        self,
        html: str
    ):


        pattern = (
            r'self\.__next_f\.push\((.*?)\)'
        )


        matches = re.findall(

            pattern,

            html,

            re.DOTALL

        )


        return matches



    def _extract_values(
        self,
        text: str
    ) -> Dict:


        values = {}



        patterns = {


            "xau_usd":

            r'(?:xau|ounce)[^0-9]{0,50}'
            r'([0-9]{3,6})',


            "gold18_price":

            r'(?:gold18|18k)[^0-9]{0,50}'
            r'([0-9]{6,12})',


            "mesghal_price":

            r'mesghal[^0-9]{0,50}'
            r'([0-9]{6,12})',


            "coin_emami":

            r'emami[^0-9]{0,50}'
            r'([0-9]{6,12})',


            "coin_bahar":

            r'bahar[^0-9]{0,50}'
            r'([0-9]{6,12})'

        }



        for name, pattern in patterns.items():


            match = re.search(

                pattern,

                text,

                re.IGNORECASE

            )


            if match:


                try:

                    values[name] = float(
                        match.group(1)
                    )

                except Exception:

                    pass



        return values
