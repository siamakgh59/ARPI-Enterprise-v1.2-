from datetime import datetime


class MacroCache:
    """
    ARPI Macro Cache Layer

    Stores last valid macro values
    to protect against temporary
    external data provider failures.
    """

    def __init__(self):

        self.storage = {}



    def set(
        self,
        key: str,
        value: float
    ):

        self.storage[key] = {

            "value": value,

            "timestamp": datetime.utcnow()

        }



    def get(
        self,
        key: str
    ):

        data = self.storage.get(
            key
        )

        if not data:

            return None


        return data



    def get_value(
        self,
        key: str
    ):

        data = self.get(
            key
        )

        if not data:

            return None


        return data.get(
            "value"
        )



    def get_age_seconds(
        self,
        key: str
    ):

        data = self.get(
            key
        )

        if not data:

            return None


        delta = (
            datetime.utcnow()
            -
            data["timestamp"]
        )


        return delta.total_seconds()



    def clear(self):

        self.storage.clear()
