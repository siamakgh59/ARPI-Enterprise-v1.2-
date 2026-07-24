# app/engines/gold/providers/faraz_scraper.py

import httpx
import re


class FarazScraper:
    """
    Faraz.io Gold Market Scraper V2

    Sources:
    1- General Gold & Currency Market
       - Mesghal
       - USD
       - Global gold references

    2- Gold 18 Karat page
       - Gold18 price

    Responsibility:
    - Fetch raw HTML pages
    - Detect Next.js payloads
    - Return raw sources

    Parsing is handled by FarazParser.
    """

    def __init__(self):

        self.urls = {

            "market":
                "https://faraz.io/markets/gold-currency",

            "gold18":
                "https://faraz.io/markets/gold-currency/geramTalaHejdah"

        }


        self.headers = {

            "User-Agent":
                (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/120 Safari/537.36"
                ),

            "Accept-Language":
                "fa-IR,fa;q=0.9,en;q=0.8"

        }



    def fetch_pages(self):

        sources = {}


        print(
            "######## FARAZ GOLD SCRAPER DEBUG ########"
        )


        for name, url in self.urls.items():

            try:

                print(
                    "FETCH SOURCE:",
                    name
                )

                print(
                    "URL:",
                    url
                )


                response = httpx.get(

                    url,

                    timeout=20,

                    headers=self.headers

                )


                response.raise_for_status()


                html = response.text


                print(
                    "HTML LENGTH:",
                    len(html)
                )


                self._detect_markers(
                    html
                )


                sources[name] = html



            except Exception as e:


                print(
                    "Faraz Fetch Error:",
                    name,
                    str(e)
                )


                sources[name] = ""



        print(
            "##########################################"
        )


        return sources



    def fetch_page(self):

        """
        Backward compatibility
        """

        pages = self.fetch_pages()


        return pages.get(
            "market",
            ""
        )



    def _detect_markers(
        self,
        html: str
    ):


        print(
            "MARKERS:"
        )


        markers = [

            "__NEXT_DATA__",

            "self.__next_f",

            "market",

            "gold",

            "rows",

            "lastPrice"

        ]


        for marker in markers:


            if marker in html:

                print(
                    "FOUND:",
                    marker
                )



        streams = re.findall(

            r'self\.__next_f\.push',

            html

        )


        print(

            "NEXT STREAM COUNT:",

            len(streams)

        )
