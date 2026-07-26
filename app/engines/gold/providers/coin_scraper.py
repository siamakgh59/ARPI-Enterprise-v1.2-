import httpx


class CoinScraper:
    """
    ARPI Coin Market Scraper v1.0

    Extract:
    - Coin Emami
    - Coin Bahar
    """

    def __init__(self):

        self.urls = {

            "coin_emami":
                "https://faraz.io/markets/gold-currency/sekkeEmami",

            "coin_bahar":
                "https://faraz.io/markets/gold-currency/sekkeBahar"

        }


        self.headers = {

            "User-Agent":
                (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )

        }



    def fetch_pages(self):

        results = {}

        print(
            "######## COIN SCRAPER ACTIVE ########"
        )


        for name, url in self.urls.items():

            try:

                response = httpx.get(
                    url,
                    headers=self.headers,
                    timeout=20
                )


                response.raise_for_status()


                results[name] = response.text


                print(
                    "FETCHED:",
                    name,
                    len(response.text)
                )


            except Exception as e:

                print(
                    "COIN FETCH ERROR:",
                    name,
                    e
                )

                results[name] = ""


        return results
