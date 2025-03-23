import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Telegram bot token loaded from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
