import streamlit as st
import subprocess
import os
import pandas as pd
import requests
import time

st.set_page_config(page_title="NitroBot Dashboard", layout="wide")

if "bot_running" not in st.session_state:
    st.session_state.bot_running = False
if "last_price" not in st.session_state:
    st.session_state.last_price = None

st.title("📊 NitroBot Dashboard")
mode = st.sidebar.selectbox("Mode", ["Demo", "Real"])
st.sidebar.write("Trading Mode:", mode)

st.subheader("💰 Live BTC/USDT Price")

def fetch_price(retries=3, delay=2):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    headers = {"User-Agent": "Mozilla/5.0"}
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                price = float(data["bitcoin"]["usd"])
                st.session_state.last_price = price
                return price
            else:
                print(f"⚠️ Status {response.status_code} on attempt {attempt+1}")
        except Exception as e:
            print(f"❌ Error on attempt {attempt+1}: {e}")
        time.sleep(delay)
    # Return cached price if API calls all fail
    return st.session_state.last_price

price = fetch_price()

if price is not None:
    st.metric("BTC/USDT", f"${price:,.2f}")
else:
    st.metric("BTC/USDT", "Unavailable")

st.subheader("📈 Realized Profit")

if os.path.exists("trade_log.csv"):
    df = pd.read_csv("trade_log.csv")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df.dropna(inplace=True)
    df["value"] = df["price"] * df["amount"]
    realized_profit = df["value"].diff().fillna(0).sum()
else:
    df = pd.DataFrame(columns=["type", "price", "amount"])
    realized_profit = 0.00

st.metric("Realized PnL", f"${realized_profit:,.2f}")
st.dataframe(df, use_container_width=True)

st.subheader("🤖 NitroBot Control")

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Start NitroBot"):
        if not st.session_state.bot_running:
            st.session_state.process = subprocess.Popen(["python3", "nitrobot.py"])
            st.session_state.bot_running = True
            st.success("NitroBot started!")

with col2:
    if st.button("🛑 Stop NitroBot"):
        if st.session_state.bot_running:
            st.session_state.process.terminate()
            st.session_state.bot_running = False
            st.warning("NitroBot stopped!")

st.write("Bot status:", "🟢 Running" if st.session_state.bot_running else "🔴 Stopped")
