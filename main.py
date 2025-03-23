from telegram.bot import TelegramBotInterface

if __name__ == '__main__':
    bot_interface = TelegramBotInterface()
    print("🤖 Bot is running...")
    bot_interface.run()
