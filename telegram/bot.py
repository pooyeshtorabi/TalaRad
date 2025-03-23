import telebot
from telebot import types
from config import TELEGRAM_TOKEN
from utils.state_manager import StateManager
from logic.investment import InvestmentAdvisor
from logic.calculator import Calculator
from telegram.handlers.main_handlers import register_handlers

class TelegramBotInterface:
    """
    A class representing the Telegram bot interface.

    Attributes:
        bot (TeleBot): Instance of the telebot.
        state_manager (StateManager): Instance for managing user states.
        investment_advisor (InvestmentAdvisor): Instance to provide investment advice.
        calculator (Calculator): Instance to compute buy and sell prices.
    """

    def __init__(self):
        """
        Initialize the TelegramBotInterface and register all message handlers.
        """
        self.bot = telebot.TeleBot(TELEGRAM_TOKEN)
        self.state_manager = StateManager()
        self.investment_advisor = InvestmentAdvisor()
        self.calculator = Calculator()
        register_handlers(self)

    def main_menu_keyboard(self):
        """
        Create the main menu keyboard.

        :return: A ReplyKeyboardMarkup object representing the main menu.
        :rtype: telebot.types.ReplyKeyboardMarkup
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("راهنمای سرمایه‌گذاری 💡", "محاسبه قیمت طلا💰")
        markup.row("نمایش قیمت‌ها 📊")
        return markup

    def back_keyboard(self):
        """
        Create a keyboard with a 'Back' button.

        :return: A ReplyKeyboardMarkup object with a 'Back' button.
        :rtype: telebot.types.ReplyKeyboardMarkup
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("بازگشت 🔙")
        return markup

    def calc_choice_keyboard(self):
        """
        Create the keyboard for choosing between buying and selling gold.

        :return: A ReplyKeyboardMarkup object with buying and selling options.
        :rtype: telebot.types.ReplyKeyboardMarkup
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("خرید طلا 🛒", "فروش طلا 💵")
        markup.row("بازگشت 🔙")
        return markup

    def run(self):
        """
        Start the bot's polling loop.
        """
        self.bot.infinity_polling()
