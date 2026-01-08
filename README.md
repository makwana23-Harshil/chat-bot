# Binance Futures Testnet Trading Bot

A Python-based trading bot for Binance USDT-M Futures Testnet with support for multiple order types.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Binance Testnet account
- API credentials from Binance Testnet

### Installation

1. **Clone the repository:**
```bash
git clone <https://github.com/makwana23-Harshil/chat-bot>
cd [chat-bot]_binance_bot
```
2, Install dependencies:
bash
Copy
pip install -r requirements.txt

3.Configure API credentials:
🔑 Getting API Keys for Binance Testnet
Step 1: Register on Binance Testnet
Visit Binance Testnet
Sign up with your email
  Complete the verification process
Step 2: Generate API Credentials
Log into your Testnet account
Go to API Management → Create API
Enter a label (e.g., "Trading Bot")
IMPORTANT: Copy and save both:
API Key
Secret Key
Step 3: Configure Your Bot
bash
Copy
# 1. Copy the example environment file
cp .env.example .env

# 2. Edit .env file with your credentials
nano .env  # or use any text editor
Add your credentials:

Copy and paste here 
API_KEY=your_testnet_api_key_here
API_SECRET=your_testnet_secret_key_here
TESTNET=true

the main file is app.py so run it 
Security note:
API credentials are loaded via enviroment variables and are not committed to the repository.

"""NOTE THAT"""
This project uses Binance Futures Testnet Only.No real funds are involved.
