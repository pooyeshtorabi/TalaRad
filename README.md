<h1 align="center">TalaRad 🪙</h1>
<p align="center">
  <img src="https://github.com/user-attachments/assets/da065264-9f8e-45d4-8a2d-43b4a311c4ec" alt="TalaRad Logo" width="300" style="border-radius: 45px;">
</p>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12.4-blue?logo=python) 
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.0.0-orange)

</div>


---
TalaRad is a modular, class-based Telegram bot that provides real-time gold price information, investment advice, and price calculations for buying and selling gold. The project fetches data from external APIs and presents actionable investment insights via a user-friendly Telegram interface. Currently, only the Telegram interface is implemented. Contributors are welcome to develop additional interfaces (e.g., web or mobile) that leverage the core logic.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

TalaRad is designed to help investors obtain up-to-date information on gold prices and make informed investment decisions. The bot retrieves data on:

- **Iranian Gold Price:** Price per gram of Iranian gold.
- **Coin Price (GCHEMM):** Local gold coin price.
- **USD Price:** Current US Dollar price.
- **International Gold Price (XAU):** Global gold price data.

Using this data, the bot calculates a ratio (coin price divided by gold price) and provides investment advice (in Persian) along with detailed reasons. It also performs calculations for final buying and selling prices based on user inputs such as gold weight and wage percentage.

---

## Features

- **Real-Time Data:** Fetches current prices from external APIs.
- **Investment Advice:** Provides personalized recommendations (e.g., "Buy Coin", "Hold", "Buy Gold") in Persian based on the computed ratio.
- **Price Calculations:** Calculates final buying and selling prices using custom formulas.
- **Modular, Class-Based Design:** Organized into separate modules for price fetching, business logic, Telegram interface, and utilities.
- **Extensible Interface:** Currently, only the Telegram interface is implemented. Additional interfaces can be developed by contributors.
- **Environment-Based Configuration:** Uses environment variables to manage sensitive data such as the Telegram bot token.

---

## Installation

Clone the repository and set up the environment. Run the following commands in your terminal:

```
git clone https://github.com/pooyeshtorabi/TalaRad.git
cd TalaRad
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

---

## Configuration

1. Create a file named `.env` in the project root directory.
2. Add your Telegram bot token to the `.env` file:

```
TELEGRAM_TOKEN=your_telegram_bot_token_here
```

The `config.py` file will automatically load these environment variables using [python-dotenv](https://pypi.org/project/python-dotenv/).

---

## Usage

To run the bot, execute the following command:

```
python main.py
```

Then, open Telegram and start a conversation with your bot. Use the `/start` command to receive a welcome message. Available options include:

![image](https://github.com/user-attachments/assets/0ba757b4-9bcd-4193-9ef9-d6f1899d423f)


- **راهنمای سرمایه‌گذاری 💡:** Get investment advice.
- **محاسبه قیمت طلا💰:** Calculate buying/selling prices.
- **نمایش قیمت‌ها 📊:** View current price data.

---

## Project Structure

The project is organized into distinct modules for clear separation of concerns:

```
my_bot/  
├── .env                      // Environment variables file  
├── config.py                 // Loads environment variables  
├── main.py                   // Entry point for the application  
├── price/  
│   ├── __init__.py           // Price module initializer  
│   └── price_api.py          // Contains the PriceAPI class for fetching prices  
├── logic/  
│   ├── __init__.py           // Logic module initializer  
│   ├── investment.py         // Contains the InvestmentAdvisor class for investment advice  
│   └── calculator.py         // Contains the Calculator class for price calculations  
├── telegram/  
│   ├── __init__.py           // Telegram package initializer  
│   ├── bot.py                // Contains the TelegramBotInterface class  
│   └── handlers/  
│       ├── __init__.py       // Handlers package initializer  
│       └── main_handlers.py  // Registers all Telegram message handlers  
└── utils/  
    ├── __init__.py           // Utilities package initializer  
    └── state_manager.py      // Contains the StateManager class for user state management
```
---

## Dependencies

The project requires the following Python packages:

- [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

All dependencies are specified in the `requirements.txt` file.

---

## Contributing

Contributions are welcome! This project is modular, and currently only the Telegram interface is implemented. Contributors are encouraged to develop additional interfaces (e.g., web or mobile) or extend existing functionality. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Follow the project's coding style, and include detailed docstrings and comments.
4. Submit a pull request with a detailed description of your changes.

For major changes, please open an issue first to discuss your ideas.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

Developed by PooyeshTorabi with ☕️ & ❤️

Enjoy using TalaRad and happy coding!
