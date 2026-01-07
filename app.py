import streamlit as st
import requests
import os
from streamlit_lottie import st_lottie
from src.client import BinanceFuturesClient

# 1. Page Configuration
st.set_page_config(page_title="Binance Alpha Bot", layout="wide", page_icon="🤖")

# 2. Professional CSS Styling (Binance Theme)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #f0b90b; /* Binance Yellow */
        color: black;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        color: #f0b90b;
    }
    .main {
        background-color: #0e1117;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Helper for Animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

lottie_anim = load_lottieurl("https://lottie.host/80613204-747d-411e-84b2-06e987c8835c/1Y5X1v6K0G.json")

# 4. App Logic
if "client" not in st.session_state:
    st.session_state.client = None

# --- SHOW LANDING PAGE IF NOT CONNECTED ---
if st.session_state.client is None:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st_lottie(lottie_anim, height=400, key="trading_anim")
    
    with col2:
        st.write("") # Spacing
        st.title("🏆 Binance Alpha Bot")
        st.subheader("Professional USDT-M Futures Trading")
        
        with st.container(border=True):
            st.info("🔐 Enter API Credentials to Unlock Dashboard")
            key_input = st.text_input("API Key", type="password")
            secret_input = st.text_input("API Secret", type="password")
            t_net = st.toggle("Use Testnet", value=True)
            
            if st.button("Initialize Secure Session"):
                if key_input and secret_input:
                    # Initialize the client
                    st.session_state.client = BinanceFuturesClient(key_input, secret_input, testnet=t_net)
                    st.rerun()
                else:
                    st.error("Missing Credentials")

# --- SHOW FULL DASHBOARD IF CONNECTED ---
else:
    # Sidebar Logout Option
    with st.sidebar:
        st.success("✅ Session Active")
        if st.button("Disconnect Bot"):
            st.session_state.client = None
            st.rerun()

    # YOUR ORIGINAL TRADING CODE STARTS HERE
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
            if os.path.exists("bot.log"):
                with open("bot.log", "r") as f:
                    st.text(f.read()[-2000:])
            else:
                st.warning("Logs will appear here once you make a trade.")
        except Exception as e:
            st.error(f"Could not read logs: {e}")
