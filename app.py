import streamlit as st
import requests
import os
import json
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
    /* Professional Offline Header Icon */
    .binance-icon {
        background-color: #f0b90b;
        color: black;
        width: 150px;
        height: 150px;
        line-height: 150px;
        border-radius: 20%;
        text-align: center;
        font-size: 80px;
        font-weight: bold;
        margin: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Helper for Local Animation
def load_lottie_local(filepath: str):
    try:
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return json.load(f)
        return None
    except Exception:
        return None

lottie_anim = load_lottie_local("src/animation.json") 

# 4. App Logic
if "client" not in st.session_state:
    st.session_state.client = None

# --- SHOW LANDING PAGE IF NOT CONNECTED ---
if st.session_state.client is None:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if lottie_anim:
            st_lottie(lottie_anim, height=400, key="trading_anim")
        else:
            # INTERNET-FREE HEADER (Fixes your missing image issue)
            st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="binance-icon">₿</div>', unsafe_allow_html=True)
            st.markdown('<h2 style="text-align:center;">OFFLINE MODE ACTIVE</h2>', unsafe_allow_html=True)

    with col2:
        st.write("") 
        st.title("🏆 Binance Alpha Bot")
        st.subheader("Professional USDT-M Futures Trading")
        
        with st.container(border=True):
            st.info("🔐 Enter API Credentials to Unlock Dashboard")
            key_input = st.text_input("API Key", type="password")
            secret_input = st.text_input("API Secret", type="password")
            t_net = st.toggle("Use Testnet", value=True)
            
            if st.button("Initialize Secure Session"):
                if key_input and secret_input:
                    st.session_state.client = BinanceFuturesClient(key_input, secret_input, testnet=t_net)
                    st.rerun()
                else:
                    st.error("Missing Credentials")

# --- SHOW FULL DASHBOARD IF CONNECTED ---
else:
    with st.sidebar:
        st.success("✅ Session Active")
        if st.button("Disconnect Bot"):
            st.session_state.client = None
            st.rerun()

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
        st.subheader("📋 Bot Activity Logs")
        if st.button("🔄 Refresh Logs"):
            st.rerun()

        if os.path.exists("bot.log"):
            try:
                with open("bot.log", "r") as f:
                    log_lines = f.readlines()
                
                if log_lines:
                    recent_logs = "".join(log_lines[-50:])
                    st.code(recent_logs, language="text", wrap_lines=True)
                    st.download_button(
                        label="📥 Download Full Log File for Report",
                        data="".join(log_lines),
                        file_name="binance_bot_logs.log",
                        mime="text/plain"
                    )
                else:
                    st.info("The log file is currently empty.")
            except Exception as e:
                st.error(f"Error reading log file: {e}")
        else:
            st.warning("⚠️ Log file 'bot.log' has not been created yet.")
