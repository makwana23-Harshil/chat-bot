import streamlit as st
import os
from src.client import BinanceFuturesClient

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Binance Alpha Bot",
    layout="wide",
    page_icon="🤖"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.stButton>button {
    width: 100%;
    border-radius: 6px;
    height: 3em;
    background-color: #f0b90b;
    color: black;
    font-weight: bold;
}

.main {
    background-color: #0e1117;
}

.card {
    background: #111827;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "client" not in st.session_state:
    st.session_state.client = None

# ================= LANDING PAGE =================
if st.session_state.client is None:

    col1, col2 = st.columns([1.2, 0.8])

    # -------- LEFT COLUMN (IMAGE) --------
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.image("assets/download.png", width=280)
        st.markdown("</div>", unsafe_allow_html=True)

    # -------- RIGHT COLUMN (LOGIN) --------
    with col2:
        st.title("🏆 Binance Alpha Bot")
        st.subheader("Professional USDT-M Futures Trading")

        with st.container(border=True):
            st.info("🔐 Enter API Credentials")

            api_key = st.text_input("API Key", type="password")
            api_secret = st.text_input("API Secret", type="password")
            testnet = st.toggle("Use Testnet", value=True)

            if st.button("Initialize Secure Session"):
                if api_key and api_secret:
                    st.session_state.client = BinanceFuturesClient(
                        api_key,
                        api_secret,
                        testnet=testnet
                    )
                    st.rerun()
                else:
                    st.error("❌ Please enter API Key and Secret")

# ================= DASHBOARD =================
else:
    client = st.session_state.client

    # -------- SIDEBAR --------
    with st.sidebar:
        st.success("✅ Session Active")
        if st.button("Disconnect Bot"):
            st.session_state.client = None
            st.rerun()

    tab1, tab2, tab3 = st.tabs(
        ["📈 Basic Orders", "⚙️ Advanced Orders", "📋 Logs"]
    )

    # -------- TAB 1: BASIC ORDERS --------
    with tab1:
        st.subheader("Market & Limit Orders")

        symbol = st.text_input("Symbol", "BTCUSDT")
        side = st.selectbox("Side", ["BUY", "SELL"])
        order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
        quantity = st.number_input("Quantity", value=0.01)
        price = st.number_input("Price (Limit only)", value=0.0)

        if st.button("Place Order"):
            response = client.place_order(
                symbol,
                side,
                order_type,
                quantity,
                price if order_type == "LIMIT" else None
            )
            st.json(response)

    # -------- TAB 2: ADVANCED --------
    with tab2:
        st.subheader("Advanced Strategies")

        strategy = st.selectbox("Strategy", ["OCO", "TWAP"])

        if strategy == "OCO":
            take_profit = st.number_input("Take Profit Price")
            stop_loss = st.number_input("Stop Loss Price")

            if st.button("Place OCO Order"):
                result = client.place_oco_order(
                    symbol, side, quantity, take_profit, stop_loss
                )
                st.json(result)

        if strategy == "TWAP":
            slices = st.slider("Order Chunks", 2, 10, 5)
            delay = st.number_input("Delay (seconds)", 10)

            if st.button("Start TWAP"):
                client.run_twap(symbol, side, quantity, slices, delay)
                st.success("✅ TWAP Completed")

    # -------- TAB 3: LOGS --------
    with tab3:
        st.subheader("Bot Activity Logs")

        if os.path.exists("bot.log"):
            with open("bot.log", "r") as f:
                logs = f.read()
            st.code(logs, language="text")
        else:
            st.warning("⚠️ No log file found")
