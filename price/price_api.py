import requests
from bs4 import BeautifulSoup

class PriceAPI:
    """
    A class to fetch and process price data from various APIs.

    Attributes:
        api_mapping (dict): Mapping of currency codes to their API URLs.
        headers (dict): HTTP headers for making the API requests.
    """
    api_mapping = {
        "USD": "https://www.tgju.org/profile/price_dollar_rl",
        "AU": "https://www.tgju.org/profile/geram18",
        "GCHEMM": "https://www.tgju.org/profile/sekee",
        "XAU": "https://www.tgju.org/profile/ons"
    }
    headers = {"User-Agent": "Mozilla/5.0"}

    def get_price(self, currency: str):
        """
        Fetch and process the price for a given currency.

        :param currency: Currency code (e.g., "USD", "AU", "GCHEMM", "XAU").
        :type currency: str
        :return: The processed price as an integer, or an error message string.
        :rtype: int or str
        """
        if currency not in self.api_mapping:
            return "Unsupported currency"
        response = requests.get(self.api_mapping[currency], headers=self.headers)
        if response.status_code != 200:
            return f"ERROR IN FETCHING {currency}"
        soup = BeautifulSoup(response.text, "html.parser")
        price_element = soup.find("span", {"data-col": "info.last_trade.PDrCotVal"})
        if not (price_element and price_element.text):
            return f"ERROR FINDING {currency} PRICE"
        try:
            raw = float(price_element.text.replace(",", ""))
        except ValueError:
            return f"ERROR PROCESSING {currency} PRICE"
        if currency in ["USD", "AU", "GCHEMM"]:
            return int(raw // 10)
        return int(raw)

    def __str__(self):
        """
        Return a string representation of all fetched prices.

        :return: A newline-separated string of currency codes and their prices.
        :rtype: str
        """
        prices = {cur: self.get_price(cur) for cur in self.api_mapping}
        return "\n".join(f"{cur}: {price}" for cur, price in prices.items())
