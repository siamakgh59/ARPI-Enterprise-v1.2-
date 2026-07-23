import httpx


class FarazScraper:
    """
    Web scraper for Faraz.io

    Responsibility:
    Only fetch raw web data.
    No intelligence logic.
    """


    def __init__(self):

        self.url = "https://faraz.io"



    def fetch_page(self):

        try:

            response = httpx.get(
                self.url,
                timeout=10
            )

            response.raise_for_status()

            return response.text


        except Exception as e:

            return {
                "error": str(e)
            }
