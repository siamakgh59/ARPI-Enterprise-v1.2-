import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Parse Faraz.io Next.js payload

    Extracts data from:
    - self.__next_f stream
    - __NEXT_DATA__

    Output:
    GoldNormalizer compatible dictionary
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


            payloads = self._extract_next_payloads(
                html
            )


            print(
                "NEXT PAYLOAD COUNT:",
                len(payloads)
            )


            for payload in payloads:


                lower = payload.lower()


                for key in self.SEARCH_KEYS:


                    if key in lower:

                        print(
                            "FOUND KEY:",
                            key
                        )


                extracted = self._extract_numbers(
                    payload
                )


                result.update(
                    extracted
                )



            # Fallback: __NEXT_DATA__

            next_data = re.search(

                r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',

                html,

                re.DOTALL

            )


            if next_data:


                try:

                    data = json.loads(
                        next_data.group(1)
                    )


                    result.update(
                        self._extract_recursive(
                            data
                        )
                    )


                except Exception:

                    pass



            print(
                "PARSER RESULT:",
                result
            )


            return result



        except Exception as e:


            print(
                "Faraz Parser Error:",
                str(e)
            )


            return {}



    def _extract_next_payloads(
        self,
        html: str
    ):


        matches = re.findall(

            r'self\.__next_f\.push\((.*?)\)</script>',

            html,

            re.DOTALL

        )


        return matches



    def _extract_numbers(
        self,
        text: str
    ) -> Dict:


        values = {}


        patterns = {

            "xau_usd":

                r'(?:xau|ounce)[^0-9]{0,30}([0-9]{3,5})',


            "gold18_price":

                r'(?:18|gold18)[^0-9]{0,30}([0-9]{6,12})',


            "mesghal_price":

                r'(?:mesghal)[^0-9]{0,30}([0-9]{6,12})',


            "coin_emami":

                r'(?:emami)[^0-9]{0,30}([0-9]{6,12})',


            "coin_bahar":

                r'(?:bahar)[^0-9]{0,30}([0-9]{6,12})',


            "usd_free_rate":

                r'(?:usd|dollar)[^0-9]{0,30}([0-9]{4,8})'

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

                except:

                    pass



        return values



    def _extract_recursive(
        self,
        obj
    ) -> Dict:


        result = {}


        if isinstance(obj, dict):


            for key, value in obj.items():

                if isinstance(
                    value,
                    (int, float)
                ):

                    result[key] = value


                else:

                    result.update(
                        self._extract_recursive(
                            value
                        )
                    )



        elif isinstance(obj, list):


            for item in obj:

                result.update(
                    self._extract_recursive(
                        item
                    )
                )


        return result
