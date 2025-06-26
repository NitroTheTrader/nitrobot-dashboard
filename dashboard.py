import streamlit as st
import subprocess
import os
import pandas as pd
import time

if "bot_running" not in st.session_state:
    st.session_state.bot_running = False

st.set_page_config(page_title="NitroBot Dashboard", layout="wide")

mode = st.sidebar.selectbox("Mode", ["Demo", "Real"])
st.sidebar.write("Trading Mode:", mode)

st.title("📊 NitroBot Dashboard")

st.subheader("Live Price Tracker")
st.write("Fetching BTC/USDT price...")
btc_price = 63000.25
st.metric("BTC/USDT", f"${btc_price:,.2f}")

st.subheader("📈 Profit Tracker")

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
st.dataframe(df)

st.subheader("🕹️ Bot Control")

if st.button("🚀 Start NitroBot"):
    if not st.session_state.bot_running:
        st.session_state.process = subprocess.Popen(["python3", "nitrobot.py"])
        st.session_state.bot_running = True
        st.success("NitroBot started!")

if st.button("🛑 Stop NitroBot"):
    if st.session_state.bot_running:
        st.session_state.process.terminate()
        st.session_state.bot_running = False
        st.warning("NitroBot stopped!")

st.write("Bot status:", "🟢 Running" if st.session_state.bot_running else "🔴 Stopped")
