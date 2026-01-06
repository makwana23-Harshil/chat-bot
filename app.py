import streamlit as st
import os
import sys

# FIX for ModuleNotFoundError: Ensure the root is in the path
sys.path.append(os.path.dirname(__file__))

# Import after path fix
from src.client import BinanceFuturesClient
from src.logger import logger

st.set_page_config(page_title="Binance Bot", layout="wide")

st.title("⚡ Binance Futures Order Bot")

# --- Sidebar Configuration ---
st.sidebar.header("API Credentials")
api_key = st.sidebar.text_input("API Key", type="password")
api_secret = st.sidebar.text_input("Secret Key", type="password")
use_testnet = st.sidebar.checkbox("Use Testnet", value=True)

if st.sidebar.button("Connect Client"):
    # This call matches the corrected __init__ in client.py
    st.session_state.client = BinanceFuturesClient(
        api_key=api_key, 
        api_secret=api_secret, 
        testnet=use_testnet
    )
    st.sidebar.success("Client Connected!")

# --- Main App Logic ---
if "client" in st.session_state and st.session_state.client:
    client = st.session_state.client
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Place Market Order")
        symbol = st.text_input("Symbol (e.g., BTCUSDT)", value="BTCUSDT").upper()
        side = st.selectbox("Side", ["BUY", "SELL"])
        qty = st.number_input("Quantity", min_value=0.001, step=0.001)
        
        if st.button("Submit Order"):
            with st.spinner("Executing..."):
                res = client.new_order(symbol=symbol, side=side, type="MARKET", quantity=qty)
                st.write(res)
                logger.info(f"Order: {side} {qty} {symbol}")
    
    with col2:
        st.subheader("Account Status")
        if st.button("Refresh Balance"):
            acc = client.get_account_info()
            st.json(acc.get("assets", []))
else:
    st.info("Please enter API keys and click Connect in the sidebar.")
