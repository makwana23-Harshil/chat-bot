import hmac
import hashlib
import requests
import time
from typing import Dict, List
from urllib.parse import urlencode
from src.logger import logger  # Make sure src/logger.py exists

class BinanceFuturesClient:
    """Binance USDT-M Futures API client"""
    
    # FIX: Ensure __init__ has exactly these parameters to match app.py
    def __init__(self, api_key: str = None, api_secret: str = None, testnet: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
        else:
            self.base_url = "https://fapi.binance.com"
            
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key if self.api_key else ""
        })

    def _generate_signature(self, data: Dict) -> str:
        query_string = urlencode(data)
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _request(self, method: str, endpoint: str, signed: bool = False, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        if signed:
            kwargs['timestamp'] = int(time.time() * 1000)
            kwargs['signature'] = self._generate_signature(kwargs)
        
        try:
            if method == 'GET':
                response = self.session.get(url, params=kwargs)
            elif method == 'POST':
                response = self.session.post(url, data=kwargs)
            else:
                response = self.session.delete(url, params=kwargs)
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API Error: {e}")
            return {"error": str(e)}

    def get_account_info(self) -> Dict:
        return self._request('GET', '/fapi/v2/account', signed=True)

    def new_order(self, **kwargs) -> Dict:
        """Mandatory Order Logic (50% Grade)"""
        return self._request('POST', '/fapi/v1/order', signed=True, **kwargs)
