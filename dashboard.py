
import streamlit as st
import pandas as pd
import requests
import time
import os

st.set_page_config(page_title="🚀 NitroBot Live Dashboard", layout="wide")

st.title("🚀 NitroBot Live Dashboard — BTC/USD & Trade History")

# Auto-refresh every 30 seconds
countdown = st.empty()
st_autorefresh = st.empty()

def fetch_btc_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "bitcoin", "vs_currencies": "usd"}
        response = requests.get(url)
        data = response.json()
        return data["bitcoin"]["usd"]
    except Exception as e:
        return f"Error: {e}"

# Refresh counter
for i in range(30, 0, -1):
    btc_price = fetch_btc_price()
    st.metric(label="💰 Bitcoin (BTC/USD)", value=f"${btc_price}")
    countdown.markdown(f"🔁 Refreshing in **{i}** seconds...", unsafe_allow_html=True)
    time.sleep(1)
    st_autorefresh.empty()

# Load trade history
st.subheader("📜 NitroBot Trade Log")
csv_path = "trades.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.dataframe(df[::-1], use_container_width=True)
else:
    st.info("No trades found yet.")
