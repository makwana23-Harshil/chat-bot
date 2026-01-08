Binance Futures Testnet Trading Bot

A Python trading bot built for the Binance USDT-M Futures Testnet. It handles multiple order types, so you can test out your strategies without risking real money.

Quick Start

What you’ll need:
- Python 3.8 or higher
- A Binance Testnet account
- Your Binance Testnet API credentials

How to set it up:

1. Clone the repo:
git clone https://github.com/makwana23-Harshil/chat-bot
cd [chat-bot]_binance_bot

2. Install the dependencies:
pip install -r requirements.txt

3. Set up your API keys:
First, grab your keys from the Binance Testnet.
- Register at the Binance Testnet site.
- Sign up with your email, finish the verification.
- After logging in, head to API Management and create a new API.
- Name it something like “Trading Bot.”
- Copy your API Key and Secret Key somewhere safe. You’ll need both.

Now, configure the bot:
- Copy the example environment file: cp .env.example .env
- Open .env in your favorite editor.
- Paste your API credentials in, like this:
API_KEY=your_testnet_api_key_here
API_SECRET=your_testnet_secret_key_here
TESTNET=true

To run the bot, just launch app.py.

A quick heads-up: The bot pulls your API keys from environment variables, so you never commit sensitive info to the repo.

And remember—this bot only works with the Binance Futures Testnet. No real money on the line here. Enjoy experimenting!
