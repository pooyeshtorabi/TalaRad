class Calculator:
    """
    A class for calculating the final buying and selling prices for gold transactions.
    """

    def calculate_buy(self, gold_price, weight, wage_percent):
        """
        Calculate the final buying price for gold.

        :param gold_price: Price per gram of Iranian gold.
        :type gold_price: int
        :param weight: Weight of gold in grams.
        :type weight: float
        :param wage_percent: Wage percentage (as a number, e.g., 2 for 2%).
        :type wage_percent: float
        :return: A dictionary containing the computed gold value, wage cost, profit, tax, and final buy price.
        :rtype: dict
        """
        value_gold = weight * gold_price
        wage_value = (wage_percent / 100) * value_gold
        profit = 0.07 * (wage_value + value_gold)
        tax = 0.09 * (profit + wage_value)
        final_buy_price = value_gold + wage_value + profit + tax
        return {
            "value_gold": value_gold,
            "wage_value": wage_value,
            "profit": profit,
            "tax": tax,
            "final_buy_price": final_buy_price
        }

    def calculate_sell(self, gold_price, weight):
        """
        Calculate the final selling price for gold.

        :param gold_price: Price per gram of Iranian gold.
        :type gold_price: int
        :param weight: Weight of gold in grams.
        :type weight: float
        :return: The final sell price.
        :rtype: float
        """
        final_sell_price = (weight * gold_price * 740) / 750
        return final_sell_price
