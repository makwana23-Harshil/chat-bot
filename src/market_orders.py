
import sys
from src.client import BinanceFuturesClient

if __name__ == "__main__":
    # Example: python src/market_orders.py BTCUSDT BUY 0.01
    symbol, side, qty = sys.argv[1], sys.argv[2], sys.argv[3]
    client = BinanceFuturesClient(api_key="KEY", api_secret="SECRET")
    client.new_order(symbol=symbol, side=side, type='MARKET', quantity=qty)
