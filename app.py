# Streamlit Dashboard for Real Crypto Updates
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

# --- Centered Logo ---
st.markdown("""
    <div style='text-align: center;'>
        <img src='logo.png' width='200'/>
    </div>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center;'>📈 Real Crypto Updates Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; font-weight: bold;'>Master Trading with Real Updates.</h4>", unsafe_allow_html=True)

# --- Fetch Live Prices from Binance (Fallback to USDT if USDC is unavailable) ---
symbols = ["BTC", "ETH", "XRP", "ADA", "QNT", "CRV", "FIL", "EGLD"]
data = []

for coin in symbols:
    symbol_usdc = f"{coin}USDC"
    symbol_usdt = f"{coin}USDT"
    price = "N/A"
    
    for symbol in [symbol_usdc, symbol_usdt]:
        try:
            response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
            if response.status_code == 200:
                price = float(response.json()['price'])
                break
        except:
            continue

    signal = "Coming Soon"
    stop_loss = "-5%"
    take_profit = "+10%"
    pair_display = f"{coin}/USDC" if price != "N/A" else f"{coin}/USDT"
    data.append([pair_display, signal, price, stop_loss, take_profit])

# --- Display Table ---
df = pd.DataFrame(data, columns=["Pair", "Signal", "Price", "Stop Loss", "Take Profit"])
st.dataframe(df, use_container_width=True)

# --- Coming Soon ---
st.markdown("---")
st.subheader("🚧 Auto-Trader Bot")
st.info("Our 100x leverage auto-trading bot is launching soon. Subscribe to get early access!")


