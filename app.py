import streamlit as st
import os
import json

# 1. Page Config (Must be the very first Streamlit command)
st.set_page_config(page_title="Binance Alpha Bot", layout="wide")

# 2. Debugging Tool (Delete this once you see the app)
st.write("Checking system files...")

# Try to import custom client
try:
    from src.client import BinanceFuturesClient
    st.sidebar.success("✅ client.py found")
except Exception as e:
    st.error(f"Cannot find src/client.py. Error: {e}")

# 3. Secure Lottie Loader
def load_lottie_local(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

# Load the animation data
anim_data = load_lottie_local("src/animation.json")

# 4. App UI
if "client" not in st.session_state:
    st.session_state.client = None

if st.session_state.client is None:
    # We use a simple layout to avoid column-crash bugs
    st.title("🏆 Binance Alpha Bot")
    
    if anim_data:
        from streamlit_lottie import st_lottie
        st_lottie(anim_data, height=200)
    else:
        st.warning("Animation file missing at src/animation.json")

    # Login Form
    with st.form("login_form"):
        api_key = st.text_input("API Key", type="password")
        api_secret = st.text_input("API Secret", type="password")
        submit = st.form_submit_button("Connect Bot")
        
        if submit:
            if api_key and api_secret:
                st.session_state.client = BinanceFuturesClient(api_key, api_secret)
                st.rerun()
            else:
                st.error("Please enter keys.")
else:
    st.success("Bot Connected!")
    if st.button("Logout"):
        st.session_state.client = None
        st.rerun()
