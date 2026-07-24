# app/engines/gold/providers/faraz_scraper.py

import httpx
import re


class FarazScraper:
    """
    Faraz.io Gold Market Scraper

    Responsibility:
    - Fetch gold market page
    - Collect raw HTML
    - Detect Next.js payloads
    - Provide raw source for parser

    No parsing logic here.
    """

    def __init__(self):

        self.url = (
            "https://faraz.io/markets/gold-currency"
        )

        self.headers = {

            "User-Agent":
                (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "Chrome/120 Safari/537.36"
                ),

            "Accept-Language":
                "fa-IR,fa;q=0.9,en;q=0.8"

        }



    def fetch_page(self):

        try:

            response = httpx.get(

                self.url,

                timeout=20,

                headers=self.headers

            )


            response.raise_for_status()


            html = response.text



            print(
                "######## FARAZ GOLD SCRAPER DEBUG ########"
            )


            print(

                "URL:",

                self.url

            )


            print(

                "HTML LENGTH:",

                len(html)

            )



            self._detect_markers(
                html
            )


            print(
                "##########################################"
            )



            return html



        except Exception as e:


            print(

                "Faraz Scraper Error:",

                str(e)

            )


            return {

                "error":

                    str(e)

            }



    def _detect_markers(
        self,
        html: str
    ):

        """
        Detect embedded application data
        """



        markers = [

            "__NEXT_DATA__",

            "self.__next_f",

            "props",

            "initialState",

            "market",

            "gold",

            "xau"

        ]



        print(
            "MARKERS:"
        )



        for marker in markers:


            if marker in html:


                print(

                    "FOUND:",

                    marker

                )



        payloads = re.findall(

            r'self\.__next_f\.push',

            html

        )



        print(

            "NEXT STREAM COUNT:",

            len(payloads)

        )
