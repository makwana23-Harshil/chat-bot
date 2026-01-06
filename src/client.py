import os, time, hmac, hashlib, requests
from urllib.parse import urlencode
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()

class BinanceFuturesClient:
    def __init__(self, testnet=True):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        self.base_url = "https://testnet.binancefuture.com" if testnet else "https://fapi.binance.com"
        self.session = requests.Session()
        self.session.headers.update({'X-MBX-APIKEY': self.api_key})

    def _generate_signature(self, data):
        query_string = urlencode(data)
        return hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def _request(self, method, endpoint, signed=False, **kwargs):
        url = f"{self.base_url}{endpoint}"
        if signed:
            kwargs['timestamp'] = int(time.time() * 1000)
            kwargs['signature'] = self._generate_signature(kwargs)
        
        response = self.session.request(method, url, params=kwargs if method == 'GET' else None, data=kwargs if method != 'GET' else None)
        logger.info(f"API Request: {method} {endpoint} | Status: {response.status_code}")
        return response.json()

    def new_order(self, symbol, side, order_type, quantity, price=None):
        """Includes mandatory input validation"""
        if not symbol or float(quantity) <= 0:
            logger.error(f"Validation Error: Invalid symbol({symbol}) or quantity({quantity})")
            raise ValueError("Validation failed.")
            
        params = {"symbol": symbol.upper(), "side": side.upper(), "type": order_type.upper(), "quantity": quantity}
        if price: params["price"] = price
        return self._request('POST', '/fapi/v1/order', signed=True, **params)
