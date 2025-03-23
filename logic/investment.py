from price.price_api import PriceAPI

class InvestmentAdvisor:
    """
    A class to compute investment advice based on fetched price data.

    Attributes:
        price_api (PriceAPI): Instance used to fetch price data.
    """

    def __init__(self):
        """
        Initialize the InvestmentAdvisor with a PriceAPI instance.
        """
        self.price_api = PriceAPI()

    def get_investment_advice(self):
        """
        Calculate investment advice using current price data.

        The method performs the following:
         - Retrieves prices for coin (GCHEMM), Iranian gold (AU), USD, and XAU.
         - Computes the ratio (coin_price / gold_price).
         - Determines advice based on the ratio using defined ranges and tolerance.
         - Calculates the international gold price and the difference with Iranian gold.

        :return: A dictionary containing all price data, computed ratio, advice, reason, 
                 international gold price, and the price difference.
        :rtype: dict
        """
        coin_price = self.price_api.get_price("GCHEMM")
        gold_price = self.price_api.get_price("AU")
        usd_price = self.price_api.get_price("USD")
        xau_price = self.price_api.get_price("XAU")

        if any(isinstance(val, str) for val in [coin_price, gold_price, usd_price, xau_price]):
            return {"error": "خطا در دریافت اطلاعات قیمت. لطفاً بعداً تلاش کنید."}

        try:
            ratio = coin_price / gold_price
        except ZeroDivisionError:
            ratio = 0

        tolerance = 0.1
        if (11.3 - tolerance) <= ratio < 11.8:
            advice = "خرید سکه امامی"
            reason = f"چون حباب سکه کاهش یافته و زمان مناسب برای خرید سکه است. (نسبت: {ratio:.2f})"
        elif 11.8 <= ratio < 12.3:
            advice = "دست نگه دارید"
            reason = f"چون بازار در تعادل است. (نسبت: {ratio:.2f})"
        elif 12.3 <= ratio < (12.8 + tolerance):
            advice = "خرید طلا"
            reason = f"چون حباب سکه افزایش یافته و زمان مناسب برای خرید طلا است. (نسبت: {ratio:.2f})"
        else:
            advice = "دست نگه دارید"
            reason = f"نسبت قیمت در بازه مشخص نشده است؛ بهتر است با مشاور صحبت کنید. (نسبت: {ratio:.2f})"

        international_gold = (xau_price * usd_price) / 41.4562
        diff_global = gold_price - international_gold

        return {
            "coin_price": coin_price,
            "gold_price": gold_price,
            "usd_price": usd_price,
            "xau_price": xau_price,
            "ratio": ratio,
            "advice": advice,
            "reason": reason,
            "international_gold": international_gold,
            "diff_global": diff_global
        }
