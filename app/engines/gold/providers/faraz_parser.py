import re
import json
from typing import Dict, Any


class FarazParser:
    """
    Parse Faraz.io Next.js payload

    Input:
        Raw HTML

    Output:
        Dictionary compatible with GoldNormalizer
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
        """
        Extract embedded Next.js data
        """


        result = {}


        try:

            # Find Next.js stream payloads

            matches = re.findall(
                r'self\.__next_f\.push\((.*?)\)</script>',
                html,
                re.DOTALL
            )


            print(
                "NEXT PAYLOAD COUNT:",
                len(matches)
            )


            for block in matches:


                text = block.lower()


                for key in self.SEARCH_KEYS:

                    if key in text:

                        print(
                            "FOUND KEY:",
                            key
                        )



            # Find __NEXT_DATA__ if exists

            next_data = re.search(

                r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',

                html,

                re.DOTALL

            )


            if next_data:


                json_data = json.loads(
                    next_data.group(1)
                )


                result.update(
                    self._extract_values(
                        json_data
                    )
                )



            return result



        except Exception as e:


            print(
                "Faraz Parser Error:",
                str(e)
            )


            return {}



    def _extract_values(
        self,
        obj
    ) -> Dict:


        values = {}


        if isinstance(
            obj,
            dict
        ):


            for key, value in obj.items():


                key_lower = key.lower()


                if any(
                    x in key_lower
                    for x in self.SEARCH_KEYS
                ):

                    if isinstance(
                        value,
                        (int, float)
                    ):

                        values[key] = value



                else:

                    values.update(
                        self._extract_values(
                            value
                        )
                    )



        elif isinstance(
            obj,
            list
        ):


            for item in obj:

                values.update(
                    self._extract_values(
                        item
                    )
                )



        return values
