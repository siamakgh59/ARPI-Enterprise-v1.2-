import httpx


class FarazScraper:
    """
    Faraz.io Web Scraper

    Responsibility:
    Only fetch raw webpage data.
    Parsing will be handled separately.
    """


    def __init__(self):

        self.url = "https://faraz.io"



    def fetch_page(self):

        try:

            response = httpx.get(
                self.url,
                timeout=10,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(compatible; ARPI Enterprise)"
                    )
                }
            )

            response.raise_for_status()


            html = response.text


            # Temporary debug
            # Shows received page structure
            print(
                "######## FARAZ SCRAPER DEBUG ########"
            )

            print(
                html[:2000]
            )

            print(
                "#####################################"
            )


            return html



        except Exception as e:

            print(
                "Faraz Scraper Error:",
                str(e)
            )

            return {
                "error": str(e)
            }
