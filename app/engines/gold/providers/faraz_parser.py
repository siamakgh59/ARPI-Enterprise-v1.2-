import re
from typing import Dict, Any


class FarazParser:

    """
    Faraz Parser DEBUG V22

    فقط برای استخراج ساختار واقعی
    Next.js Flight Payload
    """

    def parse(
        self,
        html: str,
        source: str = "market"
    ) -> Dict[str, Any]:

        result = {}

        try:

            print(
                "######## FARAZ PARSER V22 DEBUG ########"
            )

            print(
                "SOURCE:",
                source
            )


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

                if (
                    "lastPrice" in payload
                    or
                    "rows" in payload
                    or
                    "price" in payload
                    or
                    "value" in payload
                ):

                    print(
                        "========== ACTIVE PAYLOAD =========="
                    )

                    print(
                        "INDEX:",
                        index
                    )

                    print(
                        "LENGTH:",
                        len(payload)
                    )

                    print(
                        payload[:5000]
                    )

                    print(
                        "===================================="
                    )


            print(
                "FINAL RESULT:",
                result
            )


            print(
                "######################################"
            )


            return result



        except Exception as e:

            print(
                "PARSER ERROR:",
                str(e)
            )

            return {}
