from .yahoo import YahooFinanceProvider


def get_providers():

    return [
        YahooFinanceProvider()
    ]
