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

# 3. Improved Helper for Animation (With Safety Checks)
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5) # Added timeout to prevent hanging
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

lottie_anim = load_lottieurl("https://lottie.host/80613204-747d-411e-84b2-06e987c8835c/1Y5X1v6K0G.json")

# 4. App Logic
if "client" not in st.session_state:
    st.session_state.client = None

# --- SHOW LANDING PAGE IF NOT CONNECTED ---
if st.session_state.client is None:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # FIX: Only call st_lottie if lottie_anim is NOT None
        if lottie_anim:
            st_lottie(lottie_anim, height=400, key="trading_anim")
        else:
            # Fallback if the animation fails to load
            st.image("https://bin.bnbstatic.com/static/images/common/og_logo.png", width=300)
            st.warning("Running in limited UI mode (Animation could not be loaded).")
    
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
        
        # 1. Add a "Refresh" button at the top
        if st.button("🔄 Refresh Logs"):
            st.rerun()

        # 2. Check if the log file exists
        if os.path.exists("bot.log"):
            try:
                # Read the file and get the last 50 lines
                with open("bot.log", "r") as f:
                    log_lines = f.readlines()
                
                if log_lines:
                    # Join the lines and display them in a clean code block
                    # newest logs will be at the bottom
                    recent_logs = "".join(log_lines[-50:])
                    st.code(recent_logs, language="text", wrap_lines=True)
                    
                    # 3. Add a Download button for your assignment report
                    st.download_button(
                        label="📥 Download Full Log File for Report",
                        data="".join(log_lines),
                        file_name="binance_bot_logs.log",
                        mime="text/plain"
                    )
                else:
                    st.info("The log file is currently empty. Place an order to see activity!")
            except Exception as e:
                st.error(f"Error reading log file: {e}")
        else:
            # This shows if the file doesn't exist yet
            st.warning("⚠️ Log file 'bot.log' has not been created yet.")
            st.info("The file will be created automatically when the bot attempts its first trade.")
