import streamlit as st
from src.client import BinanceFuturesClient

st.title("🏆 Professional Binance Bot")

# Connect Sidebar
with st.sidebar:
    api_key = st.text_input("API Key", type="password")
    api_secret = st.text_input("Secret Key", type="password")
    if st.button("Connect"):
        st.session_state.client = BinanceFuturesClient(api_key, api_secret)
        st.success("Connected!")

if "client" in st.session_state:
    client = st.session_state.client
    
    tab1, tab2, tab3 = st.tabs(["Basic Orders", "Advanced (OCO/TWAP)", "View Logs"])

    with tab1:
        st.subheader("Market & Limit Orders")
        symbol = st.text_input("Symbol", "BTCUSDT")
        side = st.selectbox("Side", ["BUY", "SELL"])
        o_type = st.selectbox("Type", ["MARKET", "LIMIT"])
        qty = st.number_input("Quantity", value=0.01)
        price = st.number_input("Price (Limit only)", value=0.0)
        
        if st.button("Execute Basic Order"):
            res = client.place_order(symbol, side, o_type, qty, price if o_type == "LIMIT" else None)
            st.json(res)

    with tab2:
        st.subheader("Advanced Strategies")
        strat = st.selectbox("Strategy", ["OCO", "TWAP"])
        
        if strat == "OCO":
            tp = st.number_input("Take Profit Price")
            sl = st.number_input("Stop Loss Price")
            if st.button("Place OCO"):
                st.json(client.place_oco_order(symbol, side, qty, tp, sl))
        
        if strat == "TWAP":
            slices = st.slider("Chunks", 2, 10, 5)
            wait = st.number_input("Seconds between slices", 10)
            if st.button("Start TWAP"):
                client.run_twap(symbol, side, qty, slices, wait)
                st.success("TWAP Completed!")

    with tab3:
        st.subheader("bot.log Content")
        try:
            with open("bot.log", "r") as f:
                st.text(f.read()[-2000:]) # Show last 2000 chars
        except:
            st.error("Log file not found yet.")
