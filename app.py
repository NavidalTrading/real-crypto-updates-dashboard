# Streamlit Dashboard for Real Crypto Updates with Live Prices and Logo
import streamlit as st
import pandas as pd
import requests

# --- Page Config ---
st.set_page_config(page_title="Real Crypto Updates", layout="wide")

# --- Theme Toggle ---
st.sidebar.title("Real Crypto Updates")
mode = st.sidebar.radio("Theme Mode", ["Dark", "Light"])

if mode == "Light":
    st.markdown("""
        <style>
        html, body {
            background-color: #ffffff;
            color: #000000;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        html, body {
            background-color: #0e1117;
            color: #ffffff;
        }
        </style>
    """, unsafe_allow_html=True)

# --- Display Logo ---
st.image("logo.png", width=200)

# --- Header ---
st.title("📈 Real Crypto Updates Dashboard")
st.caption("Master Trading with Real Updates.")

# --- Fetch Live Prices from Binance ---
symbol_map = {
    "BTC/USDC": "btcusdc",
    "ETH/USDC": "ethusdc",
    "XRP/USDC": "xrpusdc",
    "ADA/USDC": "adausdc",
    "QNT/USDC": "qntusdc",
    "CRV/USDC": "crvusdc",
    "FIL/USDC": "filusdc",
    "EGLD/USDC": "egldusdc"
}

binance_api = "https://api.binance.com/api/v3/ticker/price?symbol={}"  # lowercase symbols

data = []
for display_name, symbol in symbol_map.items():
    try:
        response = requests.get(binance_api.format(symbol.upper()))
        price = float(response.json()['price'])
    except:
        price = "N/A"

    signal = "Loading..."  # Placeholder for future logic
    stop_loss = "-5%"
    take_profit = "+10%"
    data.append([display_name, signal, price, stop_loss, take_profit])

# --- Display Table (Theme-independent) ---
df = pd.DataFrame(data, columns=["Pair", "Signal", "Price", "Stop Loss", "Take Profit"])
st.dataframe(df, use_container_width=True)

# --- Coming Soon ---
st.markdown("---")
st.subheader("🚧 Auto-Trader Bot")
st.info("Our 100x leverage auto-trading bot is launching soon. Subscribe to get early access!")

