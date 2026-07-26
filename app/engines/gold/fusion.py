from datetime import datetime
from typing import Dict


class GoldFusion:

    """
    ARPI Gold Fusion Layer V1

    Combine:
    - Domestic Gold Data
    - Global Gold Data
    """

    def __init__(
        self,
        faraz_provider,
        global_provider
    ):

        self.faraz_provider = faraz_provider

        self.global_provider = global_provider



    def fetch_combined_data(self) -> Dict:


        domestic = (
            self.faraz_provider.fetch_gold_data()
        )


        global_data = (
            self.global_provider.fetch_global_data()
        )


        combined = {}


        combined.update(
            domestic
        )


        combined.update(
            global_data
        )


        combined[
            "timestamp"
        ] = datetime.utcnow()


        print(
            "######## GOLD FUSION ########"
        )

        print(
            combined
        )

        print(
            "#############################"
        )


        return combined
