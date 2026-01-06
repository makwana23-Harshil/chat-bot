import time, sys
from src.client import BinanceFuturesClient
from src.logger import logger

def run_twap(symbol, side, total_qty, duration_min):
    client = BinanceFuturesClient()
    slices = 5
    qty_per_slice = float(total_qty) / slices
    interval = (int(duration_min) * 60) / slices
    
    logger.info(f"Starting TWAP: {side} {total_qty} {symbol} over {duration_min}m")
    for i in range(slices):
        client.new_order(symbol, side, 'MARKET', qty_per_slice)
        if i < slices - 1: time.sleep(interval)
    logger.info("TWAP Strategy Completed Successfully.")

if __name__ == "__main__":
    # Usage: python src/advanced/twap.py BTCUSDT BUY 0.1 5
    run_twap(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
