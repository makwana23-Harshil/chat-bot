import sys
from src.client import BinanceFuturesClient

if __name__ == "__main__":
    # Usage: python src/market_orders.py BTCUSDT BUY 0.01
    client = BinanceFuturesClient()
    res = client.new_order(sys.argv[1], sys.argv[2], 'MARKET', sys.argv[3])
    print(f"Order Response: {res}")
