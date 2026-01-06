
import time
from src.client import BinanceFuturesClient

def execute_twap(client, symbol, side, total_qty, duration_secs):
    """TWAP implementation: Splits order into smaller chunks over time"""
    slices = 5
    qty_per_slice = float(total_qty) / slices
    interval = duration_secs / slices
    
    for i in range(slices):
        client.new_order(symbol=symbol, side=side, type='MARKET', quantity=qty_per_slice)
        if i < slices - 1:
            time.sleep(interval)
