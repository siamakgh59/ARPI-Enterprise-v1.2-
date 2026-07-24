import re
import json
import html as html_lib
from typing import Dict, Any


class FarazParser:
    """
    Faraz.io Next.js Payload Discovery Parser

    Phase:
    Discovery / Extraction

    Goal:
    Decode self.__next_f payloads
    and discover real market objects.
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
        "market"

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


            payloads = self._extract_next_payloads(
                html
            )


            print(
                "NEXT PAYLOAD COUNT:",
                len(payloads)
            )



            decoded_blocks = []



            for index, payload in enumerate(payloads):


                decoded = self._decode_payload(
                    payload
                )


                decoded_blocks.append(
                    decoded
                )



                lower = decoded.lower()



                found = []


                for key in self.SEARCH_KEYS:

                    if key in lower:

                        found.append(
                            key
                        )



                if found:

                    print(

                        "PAYLOAD",

                        index,

                        "FOUND:",

                        found

                    )



                    # Print small sample

                    position = lower.find(
                        found[0]
                    )


                    if position >= 0:


                        start = max(
                            0,
                            position - 100
                        )


                        end = min(
                            len(decoded),
                            position + 300
                        )


                        print(
                            "SAMPLE:",
                            decoded[start:end]
                        )



            print(
                "#####################################"
            )



            # Try extracting numbers
            # after decoding


            for block in decoded_blocks:


                extracted = self._extract_numbers(
                    block
                )


                result.update(
                    extracted
                )



            print(

                "PARSER RESULT:",

                result

            )


            print(
                "#####################################"
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


        return re.findall(

            r'self\.__next_f\.push\((.*?)\)</script>',

            html,

            re.DOTALL

        )



    def _decode_payload(
        self,
        payload: str
    ) -> str:


        try:


            text = payload



            text = html_lib.unescape(
                text
            )



            # Remove wrapping quotes

            if (
                text.startswith('"')
                and
                text.endswith('"')
            ):


                text = json.loads(
                    text
                )



            return text



        except Exception:


            return payload



    def _extract_numbers(
        self,
        text: str
    ) -> Dict:


        values = {}



        patterns = {


            "xau_usd":

            [
                r'xau.{0,50}?(\d{3,6})',
                r'ounce.{0,50}?(\d{3,6})'
            ],


            "gold18_price":

            [
                r'gold18.{0,50}?(\d{6,12})',
                r'18.{0,50}?(\d{6,12})'
            ],


            "mesghal_price":

            [
                r'mesghal.{0,50}?(\d{6,12})'
            ],


            "coin_emami":

            [
                r'emami.{0,50}?(\d{6,12})'
            ],


            "coin_bahar":

            [
                r'bahar.{0,50}?(\d{6,12})'
            ],


            "usd_free_rate":

            [
                r'usd.{0,50}?(\d{4,8})',
                r'dollar.{0,50}?(\d{4,8})'
            ]

        }



        for name, regex_list in patterns.items():


            for pattern in regex_list:


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


                        break


                    except Exception:

                        pass



        return values
