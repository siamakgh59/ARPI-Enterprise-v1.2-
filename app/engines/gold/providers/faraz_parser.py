import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Next.js Payload Parser

    Debug version:
    - Extract Next.js payloads
    - Inspect payload structure
    - Find gold related data
    - Return ARPI compatible fields
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
        "price",
        "value",
        "last"

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
                "######## FARAZ PARSER DEBUG ########"
            )

            print(
                "PAYLOAD COUNT:",
                len(payloads)
            )



            for index, payload in enumerate(payloads):


                lower = payload.lower()


                found = []


                for key in self.SEARCH_KEYS:

                    if key in lower:

                        found.append(key)



                if found:


                    print(
                        "PAYLOAD",
                        index,
                        "KEYS:",
                        found
                    )


                    print(
                        "PAYLOAD SAMPLE:",
                        payload[:1200]
                    )


                    print(
                        "--------------------------------"
                    )



                extracted = self._extract_numbers(
                    payload
                )


                if extracted:

                    print(
                        "EXTRACTED:",
                        extracted
                    )


                    result.update(
                        extracted
                    )




            # __NEXT_DATA__ fallback

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


                    recursive = self._extract_recursive(
                        data
                    )


                    print(
                        "NEXT_DATA RESULT:",
                        recursive
                    )


                    result.update(
                        recursive
                    )


                except Exception as e:

                    print(
                        "NEXT_DATA ERROR:",
                        e
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

            r'(?:xau|ounce|gold)[^0-9]{0,50}([0-9]{3,6})',



            "gold18_price":

            r'(?:gold18|18)[^0-9]{0,50}([0-9]{6,12})',



            "mesghal_price":

            r'(?:mesghal)[^0-9]{0,50}([0-9]{6,12})',



            "coin_emami":

            r'(?:emami)[^0-9]{0,50}([0-9]{6,12})',



            "coin_bahar":

            r'(?:bahar)[^0-9]{0,50}([0-9]{6,12})',



            "usd_free_rate":

            r'(?:usd|dollar)[^0-9]{0,50}([0-9]{4,8})'


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


                key_lower = str(key).lower()



                if isinstance(
                    value,
                    (int, float)
                ):


                    if any(
                        k in key_lower
                        for k in self.SEARCH_KEYS
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
