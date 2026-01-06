import streamlit as st
import os
from src.client import BinanceFuturesClient # Import your core client

st.set_page_config(page_title="Binance Futures Bot", layout="wide")

st.title("🚀 Binance Futures Trading Dashboard")

# 1. Sidebar for API Configuration
with st.sidebar:
    st.header("API Settings")
    api_key = st.text_input("API Key", type="password")
    api_secret = st.text_input("Secret Key", type="password")
    use_testnet = st.checkbox("Use Testnet", value=True)
    
    if st.button("Connect Client"):
        st.session_state.client = BinanceFuturesClient(api_key, api_secret, testnet=use_testnet)
        st.success("Client Connected!")

# 2. Main Trading Interface
if "client" in st.session_state:
    tab1, tab2 = st.tabs(["Market/Limit Orders", "Advanced (TWAP/OCO)"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            symbol = st.selectbox("Symbol", ["BTCUSDT", "ETHUSDT", "BNBUSDT"])
            side = st.radio("Side", ["BUY", "SELL"])
        with col2:
            order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
            qty = st.number_input("Quantity", min_value=0.001, step=0.001)
            price = st.number_input("Price", min_value=0.0) if order_type == "LIMIT" else None

        if st.button("Place Order"):
            # Calls your core new_order logic
            response = st.session_state.client.new_order(
                symbol=symbol, side=side, type=order_type, quantity=qty, price=price
            )
            st.json(response) # Show API response

    with tab2:
        st.subheader("Advanced Order Types (Bonus)")
        # Add inputs for TWAP or OCO here
else:
    st.warning("Please connect your API client in the sidebar to start trading.")
