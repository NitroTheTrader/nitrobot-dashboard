
import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(page_title="🚀 NitroBot Dashboard", layout="wide")

st.title("🚀 NitroBot Dashboard — Multi-Crypto Trading + Logs")

# List of coins to show
coins = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana"
}

# Function to fetch price
def fetch_price(coin_id):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": coin_id, "vs_currencies": "usd"}
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[coin_id]["usd"]
    except Exception as e:
        return f"Error: {e}"

# Display prices for all tracked coins
st.subheader("📈 Live Market Prices")
cols = st.columns(len(coins))
for i, (symbol, coin_id) in enumerate(coins.items()):
    price = fetch_price(coin_id)
    cols[i].metric(label=f"{symbol}/USD", value=f"${price}")

# Dropdown to choose pair from trades
st.subheader("📜 NitroBot Trade History")
csv_path = "trades.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    pairs = df["pair"].unique().tolist()
    selected_pair = st.selectbox("Select Trading Pair", options=pairs)
    filtered_df = df[df["pair"] == selected_pair]
    st.dataframe(filtered_df[::-1], use_container_width=True)
else:
    st.info("No trades found yet.")
