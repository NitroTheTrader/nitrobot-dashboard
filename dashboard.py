import streamlit as st
import requests
import time

# Set page title
st.set_page_config(page_title="🚀 NitroBot Pro Dashboard — Market + Bot Trades")

# Title
st.title("🚀 NitroBot Pro Dashboard — Market + Bot Trades")

# Function to get BTC price from CoinGecko
def get_btc_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return data['bitcoin']['usd']
    except Exception as e:
        return f"Error: {e}"

# Display market price
st.subheader("📈 Market Price")
btc_price = get_btc_price()
st.metric(label="Bitcoin (BTC/USD)", value=f"${btc_price}")

# Placeholder for bot trade history
st.subheader("🤖 NitroBot Trades")
st.info("No trade history available — waiting for NitroBot trades.")

# Footer
st.caption("Mobile-optimized layout enabled. Use sidebar for settings.")
