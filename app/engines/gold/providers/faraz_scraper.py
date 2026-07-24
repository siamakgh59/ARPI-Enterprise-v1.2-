import httpx
import re


class FarazScraper:
    """
    Faraz.io Gold Market Multi Page Scraper

    Sources:

    1) Gold Currency Market
       - Mesghal
       - USD
       - Coins

    2) Gold 18K Page
       - Gold18 price


    Responsibility:
    ONLY fetching HTML.
    No parsing logic.
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
                    "Chrome/120 Safari/537.36"
                ),


            "Accept-Language":
                "fa-IR,fa;q=0.9,en;q=0.8"


        }




    def fetch_page(self):

        """
        Backward compatibility
        """

        return self.fetch_market()



    def fetch_market(self):


        return self._fetch(

            self.urls["market"]

        )




    def fetch_gold18(self):


        return self._fetch(

            self.urls["gold18"]

        )





    def fetch_all(self):

        """
        Fetch all Faraz sources
        """


        return {


            "market":

                self.fetch_market(),


            "gold18":

                self.fetch_gold18()


        }




    def _fetch(
        self,
        url
    ):


        try:


            response = httpx.get(

                url,

                timeout=20,

                headers=self.headers

            )


            response.raise_for_status()



            html = response.text



            print(
                "######## FARAZ SCRAPER DEBUG ########"
            )


            print(
                "URL:",
                url
            )


            print(
                "HTML LENGTH:",
                len(html)
            )



            self._detect_markers(
                html
            )


            print(
                "######################################"
            )



            return html




        except Exception as e:


            print(
                "Faraz Scraper Error:",
                e
            )


            return {

                "error":

                    str(e)

            }





    def _detect_markers(
        self,
        html
    ):


        markers = [

            "self.__next_f",

            "__NEXT_DATA__",

            "market",

            "gold",

            "price",

            "rows"

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



        count = len(

            re.findall(

                r"self\.__next_f\.push",

                html

            )

        )



        print(

            "NEXT STREAM COUNT:",

            count

        )
