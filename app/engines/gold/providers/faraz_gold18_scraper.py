import requests
import re


class FarazGold18Scraper:
    """
    Faraz Gold 18K Scraper

    Target:
    https://faraz.io/markets/gold-currency/geramTalaHejdah

    Extract:
    - gold18_price
    - change
    - change_percent
    """


    URL = (
        "https://faraz.io/markets/gold-currency/"
        "geramTalaHejdah"
    )


    def fetch_page(self):

        try:

            headers = {

                "User-Agent":
                "Mozilla/5.0"

            }


            response = requests.get(
                self.URL,
                headers=headers,
                timeout=15
            )


            response.raise_for_status()


            print(
                "######## FARAZ GOLD18 SCRAPER DEBUG ########"
            )

            print(
                "URL:",
                self.URL
            )


            print(
                "HTML LENGTH:",
                len(response.text)
            )


            return response.text


        except Exception as e:


            print(
                "Gold18 Scraper Error:",
                e
            )


            return {
                "error": str(e)
            }



    def extract_price(
        self,
        html: str
    ):

        patterns = [

            r'"lastPrice":"([0-9,]+)"',

            r'"price":"([0-9,]+)"',

            r'lastPrice.{0,50}?([0-9]{6,})'

        ]


        for pattern in patterns:


            match = re.search(
                pattern,
                html
            )


            if match:

                value = (
                    match.group(1)
                    .replace(",", "")
                )


                try:

                    return float(value)


                except:

                    pass



        return None



    def fetch_gold18(
        self
    ):


        html = self.fetch_page()


        if isinstance(html, dict):

            return None



        price = self.extract_price(
            html
        )


        print(
            "GOLD18 PRICE:",
            price
        )


        return price
