from telebot import types

def register_handlers(bot_interface):
    """
    Registers the main message handlers for the Telegram bot.

    :param bot_interface: The instance of TelegramBotInterface.
    :type bot_interface: TelegramBotInterface
    """
    bot = bot_interface.bot
    state_manager = bot_interface.state_manager
    advisor = bot_interface.investment_advisor
    calculator = bot_interface.calculator

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        """
        Handler for the /start command. Sends a welcome message with the main menu.
        
        :param message: The incoming Telegram message.
        """
        chat_id = message.chat.id
        state_manager.set_state(chat_id, "main")
        welcome_text = (f"سلام {message.from_user.first_name} عزیز 👋\n"
                        "به ربات طلاراد خوش آمدید.\n"
                        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید 👇")
        bot.send_message(chat_id, welcome_text, reply_markup=bot_interface.main_menu_keyboard())

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        """
        General handler that routes user messages based on their current state.
        
        :param message: The incoming Telegram message.
        """
        chat_id = message.chat.id
        state_info = state_manager.get_state(chat_id)
        current_state = state_info["state"]
        text = message.text.strip()

        if text == "بازگشت 🔙":
            state_manager.set_state(chat_id, "main")
            bot.send_message(chat_id, "🔙 بازگشت به منوی اصلی.", reply_markup=bot_interface.main_menu_keyboard())
            return

        if current_state == "main":
            if text == "راهنمای سرمایه‌گذاری 💡":
                handle_consultation(bot_interface, chat_id)
            elif text == "محاسبه قیمت طلا💰":
                state_manager.set_state(chat_id, "calc_choice")
                bot.send_message(chat_id,
                                 "لطفاً انتخاب کنید:\n🛒 برای خرید طلا یا\n💵 برای فروش طلا؟",
                                 reply_markup=bot_interface.calc_choice_keyboard())
            elif text == "نمایش قیمت‌ها 📊":
                handle_report_price(bot_interface, chat_id)
            else:
                bot.send_message(chat_id,
                                 "❗️ گزینه نامشخص! لطفاً از منوی اصلی انتخاب کنید.",
                                 reply_markup=bot_interface.main_menu_keyboard())
        elif current_state == "calc_choice":
            if text in ["خرید طلا 🛒", "فروش طلا 💵"]:
                data = state_manager.get_state(chat_id)["data"]
                data["calc_type"] = "buy" if text == "خرید طلا 🛒" else "sell"
                state_manager.set_state(chat_id, "calc_weight", data)
                bot.send_message(chat_id,
                                 "لطفاً وزن طلای مورد نظر (به گرم) را وارد کنید:",
                                 reply_markup=bot_interface.back_keyboard())
            else:
                bot.send_message(chat_id,
                                 "❗️ گزینه نامشخص است. لطفاً بین خرید و فروش انتخاب کنید.",
                                 reply_markup=bot_interface.calc_choice_keyboard())
        elif current_state == "calc_weight":
            try:
                weight = float(text)
                data = state_manager.get_state(chat_id)["data"]
                data["weight"] = weight
                if data.get("calc_type") == "buy":
                    state_manager.set_state(chat_id, "calc_wage", data)
                    bot.send_message(chat_id,
                                     "لطفاً درصد اجرت (به صورت عدد، مثلاً 2 برای 2٪) را وارد کنید:",
                                     reply_markup=bot_interface.back_keyboard())
                else:
                    # For selling, calculate sell price using Calculator
                    gold_price = advisor.price_api.get_price("AU")
                    sell_price = calculator.calculate_sell(gold_price, weight)
                    bot.send_message(chat_id,
                                     f"💰 قیمت نهایی فروش: {sell_price:,.0f} تومان",
                                     reply_markup=bot_interface.back_keyboard())
                    state_manager.set_state(chat_id, "main")
            except ValueError:
                bot.send_message(chat_id, "❗️ لطفاً مقدار صحیح وزن (عدد) را وارد کنید:")
        elif current_state == "calc_wage":
            try:
                wage_percent = float(text)
                data = state_manager.get_state(chat_id)["data"]
                data["wage_percent"] = wage_percent
                weight = data.get("weight")
                gold_price = advisor.price_api.get_price("AU")
                calc_result = calculator.calculate_buy(gold_price, weight, wage_percent)
                msg = (
                    f"🔹 ارزش طلای خریداری شده: {calc_result['value_gold']:,.0f} تومان\n"
                    f"🔹 اجرت ({wage_percent}%): {calc_result['wage_value']:,.0f} تومان\n"
                    f"🔹 سود فروش طلا (7%): {calc_result['profit']:,.0f} تومان\n"
                    f"🔹 مالیات (9%): {calc_result['tax']:,.0f} تومان\n"
                    "---------------------------------------\n"
                    f"💰 قیمت نهایی خرید: {calc_result['final_buy_price']:,.0f} تومان"
                )
                bot.send_message(chat_id, msg, reply_markup=bot_interface.back_keyboard())
                state_manager.set_state(chat_id, "main")
            except ValueError:
                bot.send_message(chat_id, "❗️ لطفاً مقدار صحیح اجرت (عدد) را وارد کنید:")

    def handle_consultation(bot_interface, chat_id):
        """
        Handles the consultation process by retrieving investment advice and sending it.
        
        :param bot_interface: The TelegramBotInterface instance.
        :param chat_id: The chat ID to send the message to.
        """
        advice_info = advisor.get_investment_advice()
        if "error" in advice_info:
            bot.send_message(chat_id, advice_info["error"], reply_markup=bot_interface.main_menu_keyboard())
            return
        msg = (
            f"📊 قیمت سکه امامی: {advice_info['coin_price']:,} تومان\n"
            f"🥇 قیمت هر گرم طلای ایران: {advice_info['gold_price']:,} تومان\n"
            f"💵 قیمت دلار: {advice_info['usd_price']:,} تومان\n"
            f"🏆 انس جهانی: {advice_info['xau_price']:,} تومان\n\n"
            f"📈 قیمت جهانی (محاسبه‌شده): {int(advice_info['international_gold']):,} تومان\n"
            f"🔻 اختلاف (طلای ایران - جهانی): {int(advice_info['diff_global']):,} تومان\n\n"
            f"🔸 {advice_info['advice']}\n"
            f"💬 دلیل: {advice_info['reason']}\n"
            "-------------------------------------------------\n"
            "برای محاسبه قیمت طلا💰 از منوی اصلی استفاده کنید."
        )
        bot.send_message(chat_id, msg)

    def handle_report_price(bot_interface, chat_id):
        """
        Retrieves and sends the current price report.
        
        :param bot_interface: The TelegramBotInterface instance.
        :param chat_id: The chat ID to send the report to.
        """
        coin_price = advisor.price_api.get_price("GCHEMM")
        gold_price = advisor.price_api.get_price("AU")
        usd_price = advisor.price_api.get_price("USD")
        xau_price = advisor.price_api.get_price("XAU")
        if any(isinstance(val, str) for val in [usd_price, xau_price, gold_price, coin_price]):
            bot.send_message(chat_id,
                             "❌ خطا در دریافت برخی از اطلاعات قیمت.",
                             reply_markup=bot_interface.main_menu_keyboard())
            return
        msg = (
            f"💵 دلار: {usd_price:,} تومان\n"
            f"🏆 انس جهانی: {xau_price:,}\n"
            f"🥇 طلای ایران (۱۸ عیار): {gold_price:,} تومان\n"
            f"🪙 سکه امامی: {coin_price:,} تومان"
        )
        bot.send_message(chat_id, msg)
